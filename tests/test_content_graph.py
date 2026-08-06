from unittest.mock import patch
from urllib.error import URLError

from placement_agent_swarm.graphs.content_graph import build_content_graph
from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_content_graph_runs_complete_multi_source_workflow() -> None:
    first_source = CollectedSource.model_validate(
        {
            "title": "Purdue OWL Grammar",
            "url": "https://owl.purdue.edu/owl/general_writing/grammar/",
            "source_type": "official_learning_resource",
            "content": "Grammar learning content from Purdue OWL.",
        }
    )

    second_source = CollectedSource.model_validate(
        {
            "title": "British Council Grammar",
            "url": "https://learnenglish.britishcouncil.org/grammar",
            "source_type": "official_learning_resource",
            "content": "Grammar learning content from the British Council.",
        }
    )

    graph = build_content_graph()
    initial_state = make_agent_state(domain="communication")

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source",
        side_effect=[first_source, second_source],
    ):
        result = graph.invoke(initial_state)

    assert result["workflow_id"] == "test-001"
    assert result["status"] == WorkflowStatus.COMPLETED
    assert result["current_agent"] == "content_agent"
    assert result["next_agent"] == "end"
    assert result["error_message"] is None
    assert result["sources"] == [first_source, second_source]

    generated_content = result["generated_content"]

    assert isinstance(generated_content, str)
    assert "subject-verb agreement" in generated_content
    assert "Purdue OWL Grammar" in generated_content
    assert "British Council Grammar" in generated_content
    assert "Grammar learning content from Purdue OWL." in generated_content
    assert (
        "Grammar learning content from the British Council."
        in generated_content
    )


def test_content_graph_stops_when_domain_has_no_sources() -> None:
    graph = build_content_graph()
    initial_state = make_agent_state(domain="unknown-domain")

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source"
    ) as mock_fetch:
        result = graph.invoke(initial_state)

    assert result["workflow_id"] == "test-001"
    assert result["status"] == WorkflowStatus.FAILED
    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "end"
    assert result["sources"] == []
    assert result["generated_content"] is None
    assert result["error_message"] == (
        "No approved sources configured for domain: unknown-domain"
    )

    mock_fetch.assert_not_called()


def test_content_graph_continues_when_one_source_fails() -> None:
    successful_source = CollectedSource.model_validate(
        {
            "title": "British Council Grammar",
            "url": "https://learnenglish.britishcouncil.org/grammar",
            "source_type": "official_learning_resource",
            "content": "Grammar learning content from the British Council.",
        }
    )

    graph = build_content_graph()
    initial_state = make_agent_state(domain="communication")

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source",
        side_effect=[
            URLError("Purdue source unavailable"),
            successful_source,
        ],
    ):
        result = graph.invoke(initial_state)

    assert result["status"] == WorkflowStatus.COMPLETED
    assert result["current_agent"] == "content_agent"
    assert result["next_agent"] == "end"
    assert result["sources"] == [successful_source]
    assert result["error_message"] == (
        "Some approved sources could not be fetched: Purdue OWL Grammar"
    )

    generated_content = result["generated_content"]

    assert isinstance(generated_content, str)
    assert "British Council Grammar" in generated_content
    assert (
        "Grammar learning content from the British Council."
        in generated_content
    )


def test_content_graph_stops_when_all_sources_fail() -> None:
    graph = build_content_graph()
    initial_state = make_agent_state(domain="communication")

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source",
        side_effect=URLError("Source unavailable"),
    ) as mock_fetch:
        result = graph.invoke(initial_state)

    assert result["status"] == WorkflowStatus.FAILED
    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "end"
    assert result["sources"] == []
    assert result["generated_content"] is None
    assert result["error_message"] == (
        "All approved sources failed for domain: communication"
    )

    assert mock_fetch.call_count == 2