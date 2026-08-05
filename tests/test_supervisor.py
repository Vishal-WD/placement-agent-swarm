from placement_agent_swarm.agents.supervisor import supervisor_agent
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_supervisor_routes_to_source_agent() -> None:
    state = make_agent_state()

    result = supervisor_agent(state)

    assert result["status"] == WorkflowStatus.RUNNING
    assert result["current_agent"] == "supervisor"
    assert result["next_agent"] == "source_agent"
    assert result["error_message"] is None

    assert state.status == WorkflowStatus.CREATED
    assert state.current_agent == ""
    assert state.next_agent == ""