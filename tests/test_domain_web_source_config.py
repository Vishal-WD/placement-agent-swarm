import pytest

from placement_agent_swarm.config import (
    APPROVED_SOURCES,
    DOMAIN_WEB_SOURCE_CONFIGS,
    WebSourceConfig,
)


def test_domain_web_source_configs_match_approved_source_domains() -> None:
    assert set(DOMAIN_WEB_SOURCE_CONFIGS) == set(APPROVED_SOURCES)


def test_all_domain_web_source_configs_are_valid_models() -> None:
    for config in DOMAIN_WEB_SOURCE_CONFIGS.values():
        assert isinstance(config, WebSourceConfig)


def test_communication_domain_configuration() -> None:
    config = DOMAIN_WEB_SOURCE_CONFIGS["communication"]

    assert config.max_attempts == 3
    assert config.retry_delay_seconds == 1.0
    assert config.request_timeout_seconds == 10.0
    assert config.user_agent == "placement-agent-swarm-communication/0.1"


def test_java_domain_configuration() -> None:
    config = DOMAIN_WEB_SOURCE_CONFIGS["java"]

    assert config.max_attempts == 3
    assert config.retry_delay_seconds == 1.0
    assert config.request_timeout_seconds == 15.0
    assert config.user_agent == "placement-agent-swarm-java/0.1"


def test_domain_web_source_configs_mapping_is_immutable() -> None:
    mutable_view = DOMAIN_WEB_SOURCE_CONFIGS  # type: ignore[assignment]

    with pytest.raises(TypeError):
        mutable_view["python"] = WebSourceConfig()  # type: ignore[index]


def test_each_domain_uses_a_unique_user_agent() -> None:
    user_agents = [
        config.user_agent
        for config in DOMAIN_WEB_SOURCE_CONFIGS.values()
    ]

    assert len(user_agents) == len(set(user_agents))