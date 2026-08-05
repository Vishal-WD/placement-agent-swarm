import pytest
from pydantic import ValidationError

from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def test_agent_state_accepts_valid_data() -> None:
    state = AgentState(
        workflow_id="test-001",
        status=WorkflowStatus.CREATED,
        domain="communication",
        topic="subject-verb agreement",
        requested_output="practice_set",
        current_agent="",
        next_agent="",
    )

    assert state.workflow_id == "test-001"
    assert state.status == WorkflowStatus.CREATED
    assert state.sources == []
    assert state.error_message is None
    assert state.generated_content is None


def test_agent_state_rejects_empty_required_fields() -> None:
    with pytest.raises(ValidationError):
        AgentState(
            workflow_id="",
            status=WorkflowStatus.CREATED,
            domain="communication",
            topic="subject-verb agreement",
            requested_output="practice_set",
            current_agent="",
            next_agent="",
        )


def test_agent_state_rejects_extra_fields() -> None:
    invalid_data: dict[str, object] = {
        "workflow_id": "test-001",
        "status": WorkflowStatus.CREATED,
        "domain": "communication",
        "topic": "subject-verb agreement",
        "requested_output": "practice_set",
        "current_agent": "",
        "next_agent": "",
        "unexpected_field": "not allowed",
    }

    with pytest.raises(ValidationError):
        AgentState.model_validate(invalid_data)
