from placement_agent_swarm.graphs.content_graph import build_content_graph
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_content_graph_runs_complete_workflow() -> None:
    graph = build_content_graph()
    initial_state = make_agent_state()

    result = graph.invoke(initial_state)

    assert result["workflow_id"] == "test-001"
    assert result["status"] == WorkflowStatus.COMPLETED
    assert result["current_agent"] == "content_agent"
    assert result["next_agent"] == "end"
    assert result["error_message"] is None
    assert result["sources"] == [
        "Approved source placeholder for: subject-verb agreement"
    ]

    generated_content = result["generated_content"]

    assert isinstance(generated_content, str)
    assert "subject-verb agreement" in generated_content