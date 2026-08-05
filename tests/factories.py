from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def make_agent_state(
    *,
    workflow_id: str = "test-001",
    status: WorkflowStatus = WorkflowStatus.CREATED,
    domain: str = "communication",
    topic: str = "subject-verb agreement",
    requested_output: str = "practice_set",
    current_agent: str = "",
    next_agent: str = "",
    error_message: str | None = None,
    sources: list[CollectedSource] | None = None,
    generated_content: str | None = None,
) -> AgentState:
    return AgentState(
        workflow_id=workflow_id,
        status=status,
        domain=domain,
        topic=topic,
        requested_output=requested_output,
        current_agent=current_agent,
        next_agent=next_agent,
        error_message=error_message,
        sources=[] if sources is None else sources,
        generated_content=generated_content,
    )