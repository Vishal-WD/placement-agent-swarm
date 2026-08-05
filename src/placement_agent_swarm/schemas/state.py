from enum import StrEnum
from typing import TypedDict


class WorkflowStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentState(TypedDict):
    workflow_id: str
    status: WorkflowStatus
    domain: str
    topic: str
    requested_output: str
    current_agent: str
    next_agent: str
    error_message: str | None
    sources: list[str]
    generated_content: str | None