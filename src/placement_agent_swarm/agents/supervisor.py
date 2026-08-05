from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def supervisor_agent(state: AgentState) -> dict[str, object]:
    return {
        "status": WorkflowStatus.RUNNING,
        "current_agent": "supervisor",
        "next_agent": "source_agent",
        "error_message": None,
    }