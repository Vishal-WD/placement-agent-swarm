from placement_agent_swarm.agents.source_agent import source_agent
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_source_agent_adds_structured_source() -> None:
    state = make_agent_state(
        status=WorkflowStatus.RUNNING,
        current_agent="supervisor",
        next_agent="source_agent",
    )

    result = source_agent(state)

    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "content_agent"
    assert result["error_message"] is None

    sources = result["sources"]

    assert isinstance(sources, list)
    assert len(sources) == 1

    source = sources[0]

    assert source.title == "Approved source for subject-verb agreement"
    assert str(source.url) == "https://example.com/"
    assert source.source_type == "placeholder"
    assert source.content == (
        "Approved source placeholder content for: subject-verb agreement"
    )