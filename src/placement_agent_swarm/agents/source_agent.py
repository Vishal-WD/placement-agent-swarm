from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import AgentState


def source_agent(state: AgentState) -> dict[str, object]:
    topic = state.topic

    source = CollectedSource.model_validate(
        {
            "title": f"Approved source for {topic}",
            "url": "https://example.com/",
            "source_type": "placeholder",
            "content": f"Approved source placeholder content for: {topic}",
        }
    )

    return {
        "current_agent": "source_agent",
        "next_agent": "content_agent",
        "sources": [source],
        "error_message": None,
    }