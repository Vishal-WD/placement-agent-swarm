from placement_agent_swarm.config import (
    APPROVED_SOURCES,
    DOMAIN_WEB_SOURCE_CONFIGS,
    WebSourceConfig,
)
from placement_agent_swarm.connectors import (
    WebSourceFetchError,
    fetch_web_source,
)
from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus

DEFAULT_DOMAIN_WEB_SOURCE_CONFIG = WebSourceConfig()


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

    config = DOMAIN_WEB_SOURCE_CONFIGS.get(
        state.domain,
        DEFAULT_DOMAIN_WEB_SOURCE_CONFIG,
    )

    sources: list[CollectedSource] = []
    failed_sources: list[str] = []

    for source in source_definitions:
        try:
            collected_source = fetch_web_source(
                url=str(source.url),
                title=source.title,
                source_type=source.source_type,
                config=config,
            )
        except WebSourceFetchError:
            failed_sources.append(source.title)
            continue

        sources.append(collected_source)

    if not sources:
        return {
            "status": WorkflowStatus.FAILED,
            "current_agent": "source_agent",
            "next_agent": "end",
            "sources": [],
            "error_message": (
                f"All approved sources failed for domain: {state.domain}"
            ),
        }

    error_message = None

    if failed_sources:
        error_message = (
            "Some approved sources could not be fetched: "
            + ", ".join(failed_sources)
        )

    return {
        "current_agent": "source_agent",
        "next_agent": "content_agent",
        "sources": sources,
        "error_message": error_message,
    }