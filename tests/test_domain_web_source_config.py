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