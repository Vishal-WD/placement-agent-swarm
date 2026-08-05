from placement_agent_swarm.schemas.state import AgentState


def source_agent(state: AgentState) -> dict[str, object]:
    topic = state.topic

    return {
        "current_agent": "source_agent",
        "next_agent": "content_agent",
        "sources": [f"Approved source placeholder for: {topic}"],
        "error_message": None,
    }