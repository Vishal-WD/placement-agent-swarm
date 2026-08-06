from placement_agent_swarm.config import APPROVED_SOURCES
from placement_agent_swarm.connectors import fetch_web_source
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def source_agent(state: AgentState) -> dict[str, object]:
    source_definitions = APPROVED_SOURCES.get(state.domain, [])

    if not source_definitions:
        return {
            "status": WorkflowStatus.FAILED,
            "current_agent": "source_agent",
            "next_agent": "end",
            "sources": [],
            "error_message": (
                f"No approved sources configured for domain: {state.domain}"
            ),
        }

    sources = [
        fetch_web_source(
            url=str(source.url),
            title=source.title,
            source_type=source.source_type,
        )
        for source in source_definitions
    ]

    return {
        "current_agent": "source_agent",
        "next_agent": "content_agent",
        "sources": sources,
        "error_message": None,
    }