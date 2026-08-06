from unittest.mock import call, patch

from placement_agent_swarm.agents.source_agent import source_agent
from placement_agent_swarm.schemas.source import CollectedSource
from placement_agent_swarm.schemas.state import WorkflowStatus
from tests.factories import make_agent_state


def test_source_agent_fetches_all_approved_domain_sources() -> None:
    first_source = CollectedSource.model_validate(
        {
            "title": "Purdue OWL Grammar",
            "url": "https://owl.purdue.edu/owl/general_writing/grammar/",
            "source_type": "official_learning_resource",
            "content": "Grammar learning content from Purdue OWL.",
        }
    )

    second_source = CollectedSource.model_validate(
        {
            "title": "British Council Grammar",
            "url": "https://learnenglish.britishcouncil.org/grammar",
            "source_type": "official_learning_resource",
            "content": "Grammar learning content from the British Council.",
        }
    )

    state = make_agent_state(
        status=WorkflowStatus.RUNNING,
        current_agent="supervisor",
        next_agent="source_agent",
        domain="communication",
    )

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source",
        side_effect=[first_source, second_source],
    ) as mock_fetch:
        result = source_agent(state)

    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "content_agent"
    assert result["error_message"] is None
    assert result["sources"] == [first_source, second_source]

    assert mock_fetch.call_count == 2
    assert mock_fetch.call_args_list == [
        call(
            url="https://owl.purdue.edu/owl/general_writing/grammar/",
            title="Purdue OWL Grammar",
            source_type="official_learning_resource",
        ),
        call(
            url="https://learnenglish.britishcouncil.org/grammar",
            title="British Council Grammar",
            source_type="official_learning_resource",
        ),
    ]
def test_source_agent_fails_when_domain_has_no_approved_sources() -> None:
    state = make_agent_state(
        status=WorkflowStatus.RUNNING,
        current_agent="supervisor",
        next_agent="source_agent",
        domain="unknown-domain",
    )

    with patch(
        "placement_agent_swarm.agents.source_agent.fetch_web_source"
    ) as mock_fetch:
        result = source_agent(state)

    assert result["status"] == WorkflowStatus.FAILED
    assert result["current_agent"] == "source_agent"
    assert result["next_agent"] == "end"
    assert result["sources"] == []
    assert result["error_message"] == (
        "No approved sources configured for domain: unknown-domain"
    )

    mock_fetch.assert_not_called()