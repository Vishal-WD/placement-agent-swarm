from collections.abc import Mapping
from types import MappingProxyType

from placement_agent_swarm.config.web_source import WebSourceConfig

_DOMAIN_WEB_SOURCE_CONFIGS: dict[str, WebSourceConfig] = {
    "communication": WebSourceConfig(
        max_attempts=3,
        retry_delay_seconds=1.0,
        request_timeout_seconds=10.0,
        user_agent="placement-agent-swarm-communication/0.1",
    ),
    "java": WebSourceConfig(
        max_attempts=3,
        retry_delay_seconds=1.0,
        request_timeout_seconds=15.0,
        user_agent="placement-agent-swarm-java/0.1",
    ),
}

DOMAIN_WEB_SOURCE_CONFIGS: Mapping[str, WebSourceConfig] = MappingProxyType(
    _DOMAIN_WEB_SOURCE_CONFIGS
)