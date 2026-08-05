import pytest
from pydantic import ValidationError

from placement_agent_swarm.schemas.request import WorkflowRequest


def test_workflow_request_accepts_valid_data() -> None:
    request = WorkflowRequest(
        domain="communication",
        topic="subject-verb agreement",
        requested_output="practice_set",
    )

    assert request.domain == "communication"
    assert request.topic == "subject-verb agreement"
    assert request.requested_output == "practice_set"


def test_workflow_request_rejects_empty_fields() -> None:
    with pytest.raises(ValidationError):
        WorkflowRequest(
            domain="",
            topic="subject-verb agreement",
            requested_output="practice_set",
        )


def test_workflow_request_rejects_extra_fields() -> None:
    invalid_data: dict[str, object] = {
        "domain": "communication",
        "topic": "subject-verb agreement",
        "requested_output": "practice_set",
        "unexpected_field": "not allowed",
    }

    with pytest.raises(ValidationError):
        WorkflowRequest.model_validate(invalid_data)