"""Feishu/Lark channel implementation using lark-oapi SDK with WebSocket long connection."""

import asyncio
import json
import threading
import ssl
from collections import OrderedDict
from typing import Any

from agent.bus.events import OutboundMessage
from agent.bus.queue import MessageBus
from agent.channels.base import BaseChannel
from agent.config.schema import FeishuConfig

try:
    import lark_oapi as lark
    from lark_oapi.api.im.v1 import (
        CreateMessageRequest,
        CreateMessageRequestBody,
        CreateMessageReactionRequest,
        CreateMessageReactionRequestBody,
        Emoji,
        P2ImMessageReceiveV1,
    )

    FEISHU_AVAILABLE = True
except ImportError:
    FEISHU_AVAILABLE = False
    lark = None
    Emoji = None

# Message type display mapping
MSG_TYPE_MAP = {
    "image": "[image]",
    "audio": "[audio]",
    "file": "[file]",
    "sticker": "[sticker]",
}


class FeishuChannel(BaseChannel):
    """
    Feishu/Lark channel using WebSocket long connection.

    Uses WebSocket to receive events - no public IP or webhook required.

    Requires:
    - App ID and App Secret from Feishu Open Platform
    - Bot capability enabled
    - Event subscription enabled (im.message.receive_v1)
    """

    name = "feishu"

    def __init__(self, config: FeishuConfig, bus: MessageBus):
        super().__init__(config, bus)
        self.config: FeishuConfig = config
        self._client: Any = None
        self._ws_client: Any = None
        self._ws_thread: threading.Thread | None = None
        self._processed_message_ids: OrderedDict[str, None] = OrderedDict()  # Ordered dedup cache
        self._loop: asyncio.AbstractEventLoop | None = None

    async def start(self) -> None:
        """Start the Feishu bot with WebSocket long connection."""
        if not FEISHU_AVAILABLE:
            print("❌ Feishu SDK not installed. Run: pip install lark-oapi")
            return

        if not self.config.app_id or not self.config.app_secret:
            print("❌ Feishu app_id and app_secret not configured")
            return

        self._running = True
        self._loop = asyncio.get_running_loop()

        # Create Lark client for sending messages
        self._client = lark.Client.builder() \
            .app_id(self.config.app_id) \
            .app_secret(self.config.app_secret) \
            .log_level(lark.LogLevel.INFO) \
            .build()

        # Create event handler (only register message receive, ignore other events)
        event_handler = lark.EventDispatcherHandler.builder(
            self.config.encrypt_key or "",
            self.config.verification_token or "",
        ).register_p2_im_message_receive_v1(
            self._on_message_sync
        ).build()

        # Create WebSocket client for long connection
        self._ws_client = lark.ws.Client(
            self.config.app_id,
            self.config.app_secret,
            event_handler=event_handler,
            log_level=lark.LogLevel.INFO
        )

        # Start WebSocket client in a separate thread
        def run_ws():
            try:
                print("📡 正在建立飞书 WebSocket 长连接...")

                # Fix SSL certificate issue on macOS
                import os
                import certifi
                os.environ['SSL_CERT_FILE'] = certifi.where()
                os.environ['SSL_CERT_DIR'] = certifi.where()

                self._ws_client.start()
                print("✅ 飞书 WebSocket 长连接已建立")
            except Exception as e:
                print(f"❌ Feishu WebSocket error: {e}")

        self._ws_thread = threading.Thread(target=run_ws, daemon=True)
        self._ws_thread.start()

        print("✅ Feishu bot started with WebSocket long connection")
        print("📡 No public IP required - using WebSocket to receive events")

        # Keep running until stopped
        while self._running:
            await asyncio.sleep(1)

    async def stop(self) -> None:
        """Stop the Feishu bot."""
        self._running = False
        if self._ws_client:
            try:
                self._ws_client.stop()
            except Exception as e:
                print(f"⚠️  Error stopping WebSocket client: {e}")
        print("✅ Feishu bot stopped")

    def _add_reaction_sync(self, message_id: str, emoji_type: str) -> None:
        """Sync helper for adding reaction (runs in thread pool)."""
        try:
            request = CreateMessageReactionRequest.builder() \
                .message_id(message_id) \
                .request_body(
                    CreateMessageReactionRequestBody.builder()
                    .reaction_type(Emoji.builder().emoji_type(emoji_type).build())
                    .build()
                ).build()

            response = self._client.im.v1.message_reaction.create(request)

            if not response.success():
                print(f"⚠️  Failed to add reaction: code={response.code}, msg={response.msg}")
            else:
                print(f"✅ Added {emoji_type} reaction to message {message_id}")
        except Exception as e:
            print(f"⚠️  Error adding reaction: {e}")

    async def _add_reaction(self, message_id: str, emoji_type: str = "THUMBSUP") -> None:
        """
        Add a reaction emoji to a message (non-blocking).

        Common emoji types: THUMBSUP, OK, EYES, DONE, OnIt, HEART
        """
        if not self._client or not Emoji:
            return

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._add_reaction_sync, message_id, emoji_type)

    async def send(self, msg: OutboundMessage) -> None:
        """Send a message through Feishu."""
        if not self._client:
            print("⚠️  Feishu client not initialized")
            return

        try:
            # Determine receive_id_type based on chat_id format
            # open_id starts with "ou_", chat_id starts with "oc_"
            if msg.chat_id.startswith("oc_"):
                receive_id_type = "chat_id"
            else:
                receive_id_type = "open_id"

            # Check if content is a file path
            import os
            if msg.content.startswith("/") and os.path.isfile(msg.content):
                # Send file directly
                await self._send_file(msg.chat_id, msg.content, receive_id_type)
            else:
                # Send text message
                content = json.dumps({"text": msg.content})

                request = CreateMessageRequest.builder() \
                    .receive_id_type(receive_id_type) \
                    .request_body(
                        CreateMessageRequestBody.builder()
                        .receive_id(msg.chat_id)
                        .msg_type("text")
                        .content(content)
                        .build()
                    ).build()

                response = self._client.im.v1.message.create(request)

                if not response.success():
                    print(
                        f"❌ Failed to send Feishu message: code={response.code}, "
                        f"msg={response.msg}, log_id={response.get_log_id()}"
                    )
                else:
                    print(f"✅ Feishu message sent to {msg.chat_id}")

        except Exception as e:
            print(f"❌ Error sending Feishu message: {e}")

    async def _send_file(self, chat_id: str, file_path: str, receive_id_type: str) -> None:
        """Send a file through Feishu."""
        try:
            import os
            from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody

            if not os.path.isfile(file_path):
                print(f"❌ File not found: {file_path}")
                return

            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            # Determine file type from extension
            file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')

            # Check if it's an image
            image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}
            if file_ext in image_extensions:
                await self._send_image(chat_id, file_path, receive_id_type)
                return

            # Map file extensions to Feishu file types
            file_type_map = {
                'opus': 'opus',
                'mp4': 'mp4',
                'pdf': 'pdf',
                'doc': 'doc',
                'docx': 'doc',
                'xls': 'xls',
                'xlsx': 'xls',
            }

            file_type = file_type_map.get(file_ext, 'stream')  # Default to 'stream' for unknown types

            print(f"📤 Uploading file: {file_name} ({file_size} bytes) [type: {file_type}]...")

            # Upload file using multipart form data
            import requests

            # Get tenant access token
            auth_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            auth_data = {
                "app_id": self.config.app_id,
                "app_secret": self.config.app_secret
            }
            auth_response = requests.post(auth_url, json=auth_data)
            if not auth_response.ok:
                print(f"❌ Failed to get access token: {auth_response.text}")
                return

            access_token = auth_response.json().get("tenant_access_token")

            # Upload file
            upload_url = "https://open.feishu.cn/open-apis/im/v1/files"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            with open(file_path, 'rb') as f:
                files = {
                    'file': (file_name, f, 'application/octet-stream'),
                    'file_type': (None, file_type),
                    'file_name': (None, file_name)
                }
                upload_response = requests.post(upload_url, headers=headers, files=files)

            if not upload_response.ok:
                print(f"❌ Failed to upload file: {upload_response.text}")
                return

            upload_data = upload_response.json()
            if upload_data.get("code") != 0:
                print(f"❌ Upload error: {upload_data.get('msg')}")
                return

            file_key = upload_data.get("data", {}).get("file_key")
            print(f"✅ File uploaded! Key: {file_key}")

            # Send file message
            content = json.dumps({"file_key": file_key})

            request = CreateMessageRequest.builder() \
                .receive_id_type(receive_id_type) \
                .request_body(
                    CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("file")
                    .content(content)
                    .build()
                ).build()

            response = self._client.im.v1.message.create(request)

            if not response.success():
                print(f"❌ Failed to send file message: {response.msg}")
            else:
                print(f"✅ File sent to {chat_id}: {file_name}")

        except Exception as e:
            print(f"❌ Error sending file: {e}")

    async def _send_image(self, chat_id: str, image_path: str, receive_id_type: str) -> None:
        """Send an image through Feishu."""
        try:
            import os
            import requests
            from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody

            if not os.path.isfile(image_path):
                print(f"❌ Image not found: {image_path}")
                return

            file_size = os.path.getsize(image_path)
            file_name = os.path.basename(image_path)

            print(f"🖼️  Uploading image: {file_name} ({file_size} bytes)...")

            # Get tenant access token
            auth_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            auth_data = {
                "app_id": self.config.app_id,
                "app_secret": self.config.app_secret
            }
            auth_response = requests.post(auth_url, json=auth_data)
            if not auth_response.ok:
                print(f"❌ Failed to get access token: {auth_response.text}")
                return

            access_token = auth_response.json().get("tenant_access_token")

            # Upload image
            upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            with open(image_path, 'rb') as f:
                files = {
                    'image': (file_name, f, 'application/octet-stream'),
                    'image_type': (None, 'message')
                }
                upload_response = requests.post(upload_url, headers=headers, files=files)

            if not upload_response.ok:
                print(f"❌ Failed to upload image: {upload_response.text}")
                return

            upload_data = upload_response.json()
            if upload_data.get("code") != 0:
                print(f"❌ Upload error: {upload_data.get('msg')}")
                return

            image_key = upload_data.get("data", {}).get("image_key")
            print(f"✅ Image uploaded! Key: {image_key}")

            # Send image message
            content = json.dumps({"image_key": image_key})

            request = CreateMessageRequest.builder() \
                .receive_id_type(receive_id_type) \
                .request_body(
                    CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("image")
                    .content(content)
                    .build()
                ).build()

            response = self._client.im.v1.message.create(request)

            if not response.success():
                print(f"❌ Failed to send image message: {response.msg}")
            else:
                print(f"✅ Image sent to {chat_id}: {file_name}")

        except Exception as e:
            print(f"❌ Error sending image: {e}")

    def _on_message_sync(self, data: "P2ImMessageReceiveV1") -> None:
        """
        Sync handler for incoming messages (called from WebSocket thread).
        Schedules async handling in the main event loop.
        """
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._on_message(data), self._loop)

    async def _on_message(self, data: "P2ImMessageReceiveV1") -> None:
        """Handle incoming message from Feishu."""
        try:
            event = data.event
            message = event.message
            sender = event.sender

            # Deduplication check
            message_id = message.message_id
            if message_id in self._processed_message_ids:
                print(f"⚠️  消息去重: {message_id}")
                return
            self._processed_message_ids[message_id] = None

            # Trim cache: keep most recent 500 when exceeds 1000
            while len(self._processed_message_ids) > 1000:
                self._processed_message_ids.popitem(last=False)

            # Skip bot messages
            sender_type = sender.sender_type
            if sender_type == "bot":
                print(f"⚠️  跳过机器人消息")
                return

            sender_id = sender.sender_id.open_id if sender.sender_id else "unknown"
            chat_id = message.chat_id
            chat_type = message.chat_type  # "p2p" or "group"
            msg_type = message.message_type

            print(f"\n🔔 【飞书事件】")
            print(f"  消息ID: {message_id}")
            print(f"  发送者: {sender_id}")
            print(f"  聊天类型: {chat_type}")
            print(f"  消息类型: {msg_type}")

            # Add reaction to indicate "seen"
            await self._add_reaction(message_id, "THUMBSUP")

            # Parse message content
            if msg_type == "text":
                try:
                    content = json.loads(message.content).get("text", "")
                except json.JSONDecodeError:
                    content = message.content or ""
            else:
                content = MSG_TYPE_MAP.get(msg_type, f"[{msg_type}]")

            if not content:
                print(f"⚠️  消息内容为空")
                return

            print(f"  内容: {content}\n")

            # Forward to message bus
            reply_to = chat_id if chat_type == "group" else sender_id
            await self._handle_message(
                sender_id=sender_id,
                chat_id=reply_to,
                content=content,
                metadata={
                    "message_id": message_id,
                    "chat_type": chat_type,
                    "msg_type": msg_type,
                }
            )

        except Exception as e:
            print(f"❌ Error processing Feishu message: {e}")
