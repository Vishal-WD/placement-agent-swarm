from placement_agent_swarm.connectors import fetch_web_source
from placement_agent_swarm.schemas.state import AgentState


def source_agent(state: AgentState) -> dict[str, object]:
    source = fetch_web_source(
        url="https://example.com/",
        title=f"Approved source for {state.topic}",
        source_type="website",
    )

    return {
        "current_agent": "source_agent",
        "next_agent": "content_agent",
        "sources": [source],
        "error_message": None,
    }