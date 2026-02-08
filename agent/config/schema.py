"""Configuration schema using Pydantic."""

from pydantic import BaseModel, Field, ConfigDict


class FeishuConfig(BaseModel):
    """Feishu/Lark channel configuration using WebSocket long connection."""

    model_config = ConfigDict(populate_by_name=True)

    enabled: bool = False
    app_id: str = Field(default="", alias="appId")  # App ID from Feishu Open Platform
    app_secret: str = Field(default="", alias="appSecret")  # App Secret from Feishu Open Platform


class ChannelsConfig(BaseModel):
    """Configuration for chat channels."""

    feishu: FeishuConfig = Field(default_factory=FeishuConfig)


class AgentDefaults(BaseModel):
    """Default agent configuration."""

    model: str = "anthropic/claude-opus-4-5"
    max_tokens: int = 4096
    temperature: float = 0.7


class AgentsConfig(BaseModel):
    """Agent configuration."""

    defaults: AgentDefaults = Field(default_factory=AgentDefaults)


class ProviderConfig(BaseModel):
    """LLM provider configuration."""

    api_key: str = ""
    api_base: str | None = None


class ProvidersConfig(BaseModel):
    """Configuration for LLM providers."""

    openrouter: ProviderConfig = Field(default_factory=ProviderConfig)
    anthropic: ProviderConfig = Field(default_factory=ProviderConfig)
    openai: ProviderConfig = Field(default_factory=ProviderConfig)


class Config(BaseModel):
    """Root configuration for Minibot."""

    agents: AgentsConfig = Field(default_factory=AgentsConfig)
    channels: ChannelsConfig = Field(default_factory=ChannelsConfig)
    providers: ProvidersConfig = Field(default_factory=ProvidersConfig)
