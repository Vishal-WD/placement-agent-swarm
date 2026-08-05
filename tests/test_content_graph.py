from placement_agent_swarm.graphs.content_graph import build_content_graph
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def test_content_graph_runs_complete_workflow() -> None:
    graph = build_content_graph()

    initial_state: AgentState = {
        "workflow_id": "test-001",
        "status": WorkflowStatus.CREATED,
        "domain": "communication",
        "topic": "subject-verb agreement",
        "requested_output": "practice_set",
        "current_agent": "",
        "next_agent": "",
        "error_message": None,
        "sources": [],
        "generated_content": None,
    }

    result = graph.invoke(initial_state)

    assert result["status"] == WorkflowStatus.COMPLETED
    assert result["current_agent"] == "content_agent"
    assert result["next_agent"] == "end"

    assert result["sources"] == [
        "Approved source placeholder for: subject-verb agreement"
    ]

    assert result["generated_content"] is not None
    assert "subject-verb agreement" in result["generated_content"]