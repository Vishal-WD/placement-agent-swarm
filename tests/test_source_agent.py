from placement_agent_swarm.agents.source_agent import source_agent
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def test_source_agent_adds_source() -> None:
    state: AgentState = {
        "workflow_id": "test-001",
        "status": WorkflowStatus.RUNNING,
        "domain": "communication",
        "topic": "subject-verb agreement",
        "requested_output": "practice_set",
        "current_agent": "supervisor",
        "next_agent": "source_agent",
        "error_message": None,
        "sources": [],
        "generated_content": None,
    }

    result = source_agent(state)

    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "content_agent"
    assert result["sources"] == [
        "Approved source placeholder for: subject-verb agreement"
    ]
    assert result["error_message"] is None