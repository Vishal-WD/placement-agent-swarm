from unittest.mock import patch

from placement_agent_swarm.graphs.content_graph import build_content_graph
from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_content_graph_runs_complete_workflow() -> None:
    mocked_source = CollectedSource.model_validate(
        {
            "title": "Approved source for subject-verb agreement",
            "url": "https://example.com/",
            "source_type": "website",
            "content": "Example Domain",
        }
    )

    graph = build_content_graph()
    initial_state = make_agent_state()

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source",
        return_value=mocked_source,
    ):
        result = graph.invoke(initial_state)

    assert result["workflow_id"] == "test-001"
    assert result["status"] == WorkflowStatus.COMPLETED
    assert result["current_agent"] == "content_agent"
    assert result["next_agent"] == "end"
    assert result["error_message"] is None

    sources = result["sources"]

    assert sources == [mocked_source]

    generated_content = result["generated_content"]

    assert isinstance(generated_content, str)
    assert "subject-verb agreement" in generated_content
    assert "Approved source for subject-verb agreement" in generated_content
    assert "Example Domain" in generated_content