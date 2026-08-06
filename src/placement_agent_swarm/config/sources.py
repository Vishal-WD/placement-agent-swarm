from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SourceDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    url: HttpUrl
    source_type: str = Field(min_length=1)


APPROVED_SOURCES: dict[str, list[SourceDefinition]] = {
    "communication": [
        SourceDefinition.model_validate(
            {
                "title": "Purdue OWL Grammar",
                "url": "https://owl.purdue.edu/owl/general_writing/grammar/",
                "source_type": "official_learning_resource",
            }
        ),
        SourceDefinition.model_validate(
            {
                "title": "British Council Grammar",
                "url": "https://learnenglish.britishcouncil.org/grammar",
                "source_type": "official_learning_resource",
            }
        ),
    ],
    "java": [
        SourceDefinition.model_validate(
            {
                "title": "Java Documentation",
                "url": "https://docs.oracle.com/en/java/",
                "source_type": "official_documentation",
            }
        ),
        SourceDefinition.model_validate(
            {
                "title": "Java Tutorials",
                "url": "https://docs.oracle.com/javase/tutorial/",
                "source_type": "official_documentation",
            }
        ),
    ],
}