from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from placement_agent_swarm.schemas.source import CollectedSource


class WorkflowStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: str = Field(min_length=1)
    status: WorkflowStatus
    domain: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    requested_output: str = Field(min_length=1)
    current_agent: str
    next_agent: str
    error_message: str | None = None
    sources: list[CollectedSource] = Field(default_factory=list)
    generated_content: str | None = None