"""Message bus for inter-component communication."""

import asyncio
from typing import Callable

from agent.bus.events import InboundMessage, OutboundMessage


class MessageBus:
    """
    Central message bus for decoupled communication between channels and agent.

    Provides two-way async queues:
    - inbound: Messages from channels to agent
    - outbound: Messages from agent to channels
    """

    def __init__(self):
        self.inbound: asyncio.Queue[InboundMessage] = asyncio.Queue()
        self.outbound: asyncio.Queue[OutboundMessage] = asyncio.Queue()
        self._outbound_subscribers: dict[str, list[Callable]] = {}

    # ========== Inbound Flow (Channel → Agent) ==========

    async def publish_inbound(self, msg: InboundMessage) -> None:
        """Publish an inbound message from a channel."""
        await self.inbound.put(msg)

    async def consume_inbound(self) -> InboundMessage:
        """Consume an inbound message (blocking)."""
        return await self.inbound.get()

    def inbound_qsize(self) -> int:
        """Get the size of the inbound queue."""
        return self.inbound.qsize()

    # ========== Outbound Flow (Agent → Channel) ==========

    async def publish_outbound(self, msg: OutboundMessage) -> None:
        """Publish an outbound message to a channel."""
        await self.outbound.put(msg)

    async def consume_outbound(self) -> OutboundMessage:
        """Consume an outbound message (blocking)."""
        return await self.outbound.get()

    def outbound_qsize(self) -> int:
        """Get the size of the outbound queue."""
        return self.outbound.qsize()

    # ========== Utilities ==========

    def clear(self) -> None:
        """Clear all queues."""
        while not self.inbound.empty():
            try:
                self.inbound.get_nowait()
            except asyncio.QueueEmpty:
                break

        while not self.outbound.empty():
            try:
                self.outbound.get_nowait()
            except asyncio.QueueEmpty:
                break
