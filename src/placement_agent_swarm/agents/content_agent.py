from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def content_agent(state: AgentState) -> dict[str, object]:
    topic = state.topic

    source_summary = "\n".join(
        f"- {source.title}: {source.content}" for source in state.sources
    )

    generated_content = (
        f"Topic: {topic}\n"
        f"Sources:\n{source_summary}\n"
        "Generated content placeholder."
    )

    return {
        "status": WorkflowStatus.COMPLETED,
        "current_agent": "content_agent",
        "next_agent": "end",
        "generated_content": generated_content,
        "error_message": state.error_message,
    }