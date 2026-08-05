from placement_agent_swarm.agents.supervisor import supervisor_agent
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def test_supervisor_routes_to_source_agent() -> None:
    state: AgentState = {
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

    result = supervisor_agent(state)

    assert state["status"] == WorkflowStatus.CREATED
    assert result["status"] == WorkflowStatus.RUNNING
    assert result["current_agent"] == "supervisor"
    assert result["next_agent"] == "source_agent"