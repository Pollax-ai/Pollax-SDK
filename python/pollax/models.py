"""Pydantic models for Pollax API"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class Agent(BaseModel):
    """AI Agent model"""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    description: Optional[str] = None
    system_prompt: str
    provider: Literal["openai", "anthropic", "ollama"] = "openai"
    model: str = "gpt-4"
    voice_provider: Optional[Literal["elevenlabs", "openai", "google"]] = None
    voice_id: Optional[str] = None
    stt_provider: Optional[Literal["deepgram", "whisper", "google"]] = "deepgram"
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    is_active: bool = True
    tenant_id: str
    config: Optional[Dict[str, Any]] = None
    knowledge_base_ids: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    calls_count: Optional[int] = None
    success_rate: Optional[str] = None
    avg_duration: Optional[str] = None


# Call lifecycle status. Matches values emitted by the Pollax backend.
# 1.0.0 incorrectly used hyphenated values ('in-progress','no-answer') and
# 'queued' — corrected in 1.1.0 to mirror server emission.
CallStatus = Literal[
    "initiated",
    "ringing",
    "in_progress",
    "completed",
    "failed",
    "busy",
    "no_answer",
    "voicemail",
]


class Call(BaseModel):
    """Voice call model"""

    call_sid: str
    agent_id: str
    to_number: str
    from_number: Optional[str] = None
    status: CallStatus
    direction: Literal["inbound", "outbound"]
    duration: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    agent_name: Optional[str] = None


class Contact(BaseModel):
    """Campaign contact model"""

    name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Campaign(BaseModel):
    """Campaign model"""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    status: Optional[Literal["draft", "scheduled", "running", "paused", "completed", "cancelled"]] = None
    scheduled_time: Optional[datetime] = None
    contacts: List[Contact] = Field(default_factory=list)
    total_contacts: int = 0
    completed_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    tenant_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class KnowledgeDocument(BaseModel):
    """Knowledge base document model"""

    model_config = ConfigDict(extra="allow")

    id: str
    name: Optional[str] = None
    type: Optional[Literal["pdf", "txt", "docx", "url"]] = None
    content: Optional[str] = None
    url: Optional[str] = None
    chunks_count: int = 0
    status: Optional[Literal["processing", "ready", "failed"]] = None
    tenant_id: Optional[str] = None
    created_at: Optional[datetime] = None
    agent_id: Optional[str] = None


class DashboardStats(BaseModel):
    """Dashboard statistics model"""

    total_calls: int
    active_agents: int
    success_rate: str
    avg_duration: str
    calls_by_status: Dict[str, int]


class Integration(BaseModel):
    """Integration model"""

    id: str
    name: str
    type: Literal["twilio", "salesforce", "hubspot", "slack", "zapier", "webhook"]
    config: Dict[str, Any]
    is_active: bool
    tenant_id: str
    created_at: datetime
    updated_at: datetime


class PhoneNumber(BaseModel):
    """Phone number model"""

    model_config = ConfigDict(extra="allow")

    id: str
    phone_number: str
    country_code: Optional[str] = None
    capabilities: Optional[Dict[str, bool]] = None
    is_active: Optional[bool] = True
    tenant_id: Optional[str] = None
    created_at: Optional[datetime] = None
    agent_id: Optional[str] = None
    auto_renew: Optional[bool] = None
    status: Optional[str] = None


class ApiKey(BaseModel):
    """API key model"""

    id: str
    name: str
    key_prefix: str
    last_used_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime


class VoiceProfile(BaseModel):
    """Voice cloning profile model"""

    id: str
    name: str
    description: Optional[str] = None
    voice_id: str
    provider: Literal["elevenlabs", "openai"]
    status: Literal["training", "ready", "failed"]
    tenant_id: str
    created_at: datetime
