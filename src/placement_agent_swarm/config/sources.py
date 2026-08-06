from collections.abc import Mapping
from types import MappingProxyType

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from placement_agent_swarm.schemas.source import SourceType


class SourceDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(min_length=1)
    url: HttpUrl
    source_type: SourceType


_APPROVED_SOURCES: dict[str, tuple[SourceDefinition, ...]] = {
    "communication": (
        SourceDefinition.model_validate(
            {
                "title": "Purdue OWL Grammar",
                "url": "https://owl.purdue.edu/owl/general_writing/grammar/",
                "source_type": SourceType.OFFICIAL_LEARNING_RESOURCE,
            }
        ),
        SourceDefinition.model_validate(
            {
                "title": "British Council Grammar",
                "url": "https://learnenglish.britishcouncil.org/grammar",
                "source_type": SourceType.OFFICIAL_LEARNING_RESOURCE,
            }
        ),
    ),
    "java": (
        SourceDefinition.model_validate(
            {
                "title": "Java Documentation",
                "url": "https://docs.oracle.com/en/java/",
                "source_type": SourceType.OFFICIAL_DOCUMENTATION,
            }
        ),
        SourceDefinition.model_validate(
            {
                "title": "Java Tutorials",
                "url": "https://docs.oracle.com/javase/tutorial/",
                "source_type": SourceType.OFFICIAL_DOCUMENTATION,
            }
        ),
    ),
}

APPROVED_SOURCES: Mapping[str, tuple[SourceDefinition, ...]] = MappingProxyType(
    _APPROVED_SOURCES
)