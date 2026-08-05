from placement_agent_swarm.agents.content_agent import content_agent
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_content_agent_generates_content() -> None:
    state = make_agent_state(
        status=WorkflowStatus.RUNNING,
        current_agent="source_agent",
        next_agent="content_agent",
        sources=[
            "Approved source placeholder for: subject-verb agreement"
        ],
    )

    result = content_agent(state)

    assert result["status"] == WorkflowStatus.COMPLETED
    assert result["current_agent"] == "content_agent"
    assert result["next_agent"] == "end"
    assert result["error_message"] is None

    generated_content = result["generated_content"]

    assert isinstance(generated_content, str)
    assert "subject-verb agreement" in generated_content
    assert "Approved source placeholder" in generated_content