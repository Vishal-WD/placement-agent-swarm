from placement_agent_swarm.agents.content_agent import content_agent
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def test_content_agent_generates_content() -> None:
    state = AgentState(
        workflow_id="test-001",
        status=WorkflowStatus.RUNNING,
        domain="communication",
        topic="subject-verb agreement",
        requested_output="practice_set",
        current_agent="source_agent",
        next_agent="content_agent",
        error_message=None,
        sources=[
            "Approved source placeholder for: subject-verb agreement"
        ],
        generated_content=None,
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