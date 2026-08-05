from unittest.mock import patch

from placement_agent_swarm.agents.source_agent import source_agent
from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_source_agent_fetches_structured_web_source() -> None:
    mocked_source = CollectedSource.model_validate(
        {
            "title": "Approved source for subject-verb agreement",
            "url": "https://example.com/",
            "source_type": "website",
            "content": "Example Domain",
        }
    )

    state = make_agent_state(
        status=WorkflowStatus.RUNNING,
        current_agent="supervisor",
        next_agent="source_agent",
    )

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source",
        return_value=mocked_source,
    ) as mock_fetch:
        result = source_agent(state)

    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "content_agent"
    assert result["error_message"] is None
    assert result["sources"] == [mocked_source]

    mock_fetch.assert_called_once_with(
        url="https://example.com/",
        title="Approved source for subject-verb agreement",
        source_type="website",
    )