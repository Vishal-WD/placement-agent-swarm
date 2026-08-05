# Placement Agent Swarm

A research-oriented, production-structured agentic AI system that collects trusted placement-preparation resources, validates and processes them, and generates structured learning content for students.

## Overview

Placement-preparation resources are distributed across websites, documents, APIs, company portals, learning platforms, and communication channels. Students often spend more time searching for reliable material than preparing for placements.

Placement Agent Swarm addresses this problem through a coordinated multi-agent workflow. The system accepts a student's learning request, identifies suitable sources, collects and cleans the content, validates the resulting data, and passes it to specialized agents that generate useful preparation material.

Rather than relying on a single chatbot-style workflow, the project separates responsibilities across dedicated agents and reusable connectors.

## Key Features

- Structured request validation with Pydantic
- Typed shared state for LangGraph workflows
- Supervisor, source, and content agents
- Live web-content ingestion
- HTML cleaning with CSS and JavaScript removal
- Validated source metadata and content models
- Modular connector architecture
- Automated testing with Pytest
- Static analysis with Ruff and MyPy
- Pre-commit quality checks
- Extensible design for future specialist agents and data sources

## Problem Statement

Placement candidates commonly face the following challenges:

- Learning materials are distributed across multiple platforms.
- The reliability of online content is difficult to verify.
- Students repeatedly search for the same topics.
- Resources are not organized according to placement requirements.
- Generic AI responses may not provide source traceability.
- Different placement areas require different preparation strategies.
- Students need practice material in multiple output formats.

The system is intended to support preparation areas such as:

- Quantitative aptitude
- Logical reasoning
- Verbal ability
- Communication
- Programming
- Data structures and algorithms
- SQL and databases
- Core computer science subjects
- Technical interviews
- HR interviews
- Company-specific preparation

## Proposed Solution

The system accepts a structured request containing a domain, topic, and requested output type.

```json
{
  "domain": "communication",
  "topic": "subject-verb agreement",
  "requested_output": "practice_set"
}
```

The request is validated and converted into workflow state. The agents then:

1. Validate and interpret the request.
2. Route the task through the workflow.
3. Select approved sources.
4. Collect source content.
5. Remove unwanted HTML, CSS, and JavaScript.
6. Validate source metadata.
7. Store the collected sources in structured form.
8. Generate the requested learning content.
9. Return the result with source traceability.

## Current Workflow

```text
START
  │
  ▼
Supervisor Agent
  │
  ▼
Source Agent
  │
  ▼
Content Agent
  │
  ▼
END
```

### Supervisor Agent

The Supervisor Agent controls workflow routing and execution state.

**Current responsibilities**

- Marks the workflow as running.
- Identifies itself as the current agent.
- Routes the workflow to the Source Agent.
- Maintains workflow error information.

**Planned responsibilities**

- Analyze request complexity.
- Select specialist agents.
- Handle conditional routing.
- Retry failed tasks.
- Stop unsafe or invalid operations.
- Coordinate parallel agents.

### Source Agent

The Source Agent collects and prepares external information.

**Current responsibilities**

- Calls the web-source connector.
- Fetches live website content.
- Receives a validated `CollectedSource` object.
- Stores collected sources in workflow state.
- Routes execution to the Content Agent.

**Planned responsibilities**

- Select sources based on domain.
- Collect from multiple websites.
- Call public APIs.
- Read RSS feeds.
- Process local files and PDFs.
- Skip unavailable sources safely.
- Remove duplicate content.
- Rank sources by trust and relevance.

### Content Agent

The Content Agent transforms collected sources into student-ready output.

**Current responsibilities**

- Reads structured sources.
- Combines source titles and content.
- Produces a basic structured response.
- Marks the workflow as completed.

**Planned responsibilities**

- Generate practice questions.
- Generate explanations and examples.
- Create interview questions.
- Create revision notes.
- Generate mock assessments.
- Adapt difficulty levels.
- Produce company-specific preparation plans.
- Add citations to generated content.

## Architecture

```text
┌───────────────────────────┐
│       Student Request     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      WorkflowRequest      │
│     Pydantic Validation   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│        AgentState         │
│  Shared Workflow Context  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Supervisor Agent      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Source Agent        │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    Web Source Connector   │
│   Fetch → Decode → Clean  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      CollectedSource      │
│  Structured Source Model  │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       Content Agent       │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     Generated Content     │
└───────────────────────────┘
```

## Data Models

### `WorkflowRequest`

`WorkflowRequest` represents the external input used to start a workflow.

```python
class WorkflowRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    requested_output: str = Field(min_length=1)
```

It ensures that:

- Required fields are present.
- Required strings are not empty.
- Unexpected fields are rejected.

### `AgentState`

`AgentState` represents the typed shared state passed through the LangGraph workflow.

It currently stores:

- Workflow ID
- Workflow status
- Domain
- Topic
- Requested output
- Current agent
- Next agent
- Error message
- Collected sources
- Generated content

### `CollectedSource`

Every collected source is stored using a validated model.

```python
class CollectedSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    url: HttpUrl
    source_type: str = Field(min_length=1)
    content: str = Field(min_length=1)
```

This creates a common source contract for all connectors.

Supported or planned source types include:

- Website
- Official documentation
- Public API
- RSS feed
- Local file
- PDF document
- Company portal
- Educational resource

## Web Source Connector

The project currently includes its first real ingestion connector.

The web connector can:

- Send a live HTTP request.
- Use a custom user agent.
- Apply a network timeout.
- Read response bytes.
- Decode UTF-8 content.
- Handle invalid decoding characters.
- Parse HTML.
- Remove HTML tags.
- Ignore CSS inside `<style>` elements.
- Ignore JavaScript inside `<script>` elements.
- Return a validated `CollectedSource` object.

Current public connector functions:

- `extract_text_from_html()`
- `fetch_web_source()`

Example:

```python
from placement_agent_swarm.connectors import fetch_web_source

source = fetch_web_source(
    url="https://example.com/",
    title="Example Domain",
    source_type="website",
)

print(source.title)
print(source.url)
print(source.content)
```

## Project Structure

```text
placement-agent-swarm/
│
├── src/
│   └── placement_agent_swarm/
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── supervisor.py
│       │   ├── source_agent.py
│       │   └── content_agent.py
│       ├── connectors/
│       │   ├── __init__.py
│       │   └── web_source.py
│       ├── graphs/
│       │   ├── __init__.py
│       │   └── content_graph.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── request.py
│       │   ├── source.py
│       │   └── state.py
│       ├── config/
│       │   └── __init__.py
│       ├── __init__.py
│       ├── main.py
│       ├── quality.py
│       └── py.typed
│
├── tests/
│   ├── __init__.py
│   ├── factories.py
│   ├── test_content_agent.py
│   ├── test_content_graph.py
│   ├── test_request.py
│   ├── test_source_agent.py
│   ├── test_source_schema.py
│   ├── test_state.py
│   ├── test_supervisor.py
│   └── test_web_source.py
│
├── .pre-commit-config.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Technology Stack

| Category | Technologies |
|---|---|
| Core language | Python 3.11 |
| Agent orchestration | LangGraph, LangChain |
| Validation and configuration | Pydantic, Pydantic Settings, python-dotenv |
| Data collection | `urllib.request`, `HTMLParser` |
| Testing | Pytest, `unittest.mock` |
| Code quality | Ruff, MyPy, Pre-commit |
| Dependency management | uv |
| Version control | Git, GitHub |

## Engineering Principles

### Validated Boundaries

External requests and collected source data are validated with Pydantic before entering the workflow.

### Structured State

Agents communicate through a typed shared state instead of unstructured dictionaries.

### Separation of Responsibilities

Agents, connectors, schemas, graphs, and tests are organized into separate modules.

### Test Isolation

Live network calls are mocked during automated tests.

### Type Safety

Application and test code are checked with MyPy.

### Automated Quality Control

Every commit can run the following checks through pre-commit hooks:

- Ruff
- MyPy
- Pytest

### Extensibility

New agents and connectors can be added without rewriting the complete workflow.

## Testing Status

Current automated test count:

```text
17 passing tests
```

The tests cover:

- Workflow request validation
- Workflow state validation
- Structured source validation
- Empty-field rejection
- Extra-field rejection
- Invalid URL rejection
- Supervisor Agent routing
- Source Agent behavior
- Content Agent behavior
- Full LangGraph workflow execution
- Web connector behavior
- HTML tag removal
- CSS removal
- JavaScript removal
- Connector mocking
- Structured source propagation

Run all quality checks:

```bash
uv run quality-check
```

Run only the tests:

```bash
uv run pytest -v
```

Run Ruff:

```bash
uv run ruff check .
```

Run MyPy:

```bash
uv run mypy src tests
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Vishal-WD/placement-agent-swarm.git
cd placement-agent-swarm
```

### 2. Install `uv`

Install `uv` using the official installation method for your operating system, then verify it:

```bash
uv --version
```

### 3. Create and synchronize the environment

```bash
uv sync
```

### 4. Activate the environment when required

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install pre-commit hooks

```bash
uv run pre-commit install
```

### 6. Run the quality pipeline

```bash
uv run quality-check
```

## Running the Workflow

Run the current workflow with:

```bash
uv run python -m placement_agent_swarm.main
```

The workflow currently:

1. Creates an initial placement-preparation request.
2. Passes it to the Supervisor Agent.
3. Routes it to the Source Agent.
4. Fetches web content.
5. Converts the content into a structured source.
6. Passes it to the Content Agent.
7. Produces a basic generated response.
8. Marks the workflow as completed.

## Development Progress

| Area | Estimated completion |
|---|---:|
| Overall project | 40% |
| Engineering foundation | 85% |
| Schemas and validation | 90% |
| Testing and quality system | 85% |
| LangGraph orchestration | 45% |
| Real data ingestion | 30% |
| Multi-source ingestion | 10% |
| Intelligent content generation | 15% |
| Persistence layer | 0% |
| API and user interface | 0% |

> These values are development estimates and will change as the project scope evolves.

## Completed Milestones

- [x] Initialize the Python project
- [x] Configure `uv`
- [x] Create the LangGraph workflow
- [x] Add Supervisor Agent
- [x] Add Source Agent
- [x] Add Content Agent
- [x] Add typed workflow state
- [x] Add workflow request validation
- [x] Add structured source validation
- [x] Add shared test factories
- [x] Add Ruff
- [x] Add MyPy
- [x] Add Pytest
- [x] Add pre-commit hooks
- [x] Add automated quality pipeline
- [x] Add web source connector
- [x] Add HTML text extraction
- [x] Ignore CSS and JavaScript content
- [x] Integrate the connector with the Source Agent
- [x] Verify a live website fetch
- [x] Add agent and graph integration tests

## Roadmap

- [ ] Create an approved source registry
- [ ] Map placement domains to trusted sources
- [ ] Collect from multiple websites in one workflow
- [ ] Add connector-level exception handling
- [ ] Add retry and timeout policies
- [ ] Skip failed sources safely
- [ ] Add duplicate-content detection
- [ ] Add source trust scoring
- [ ] Add source relevance ranking
- [ ] Add public API connector
- [ ] Add RSS connector
- [ ] Add local file connector
- [ ] Add PDF connector
- [ ] Store collected data
- [ ] Add database integration
- [ ] Add LLM-based content generation
- [ ] Add citations to generated content
- [ ] Add conditional LangGraph routing
- [ ] Add specialist placement agents
- [ ] Add FastAPI service layer
- [ ] Add observability and workflow tracing
- [ ] Add Docker support
- [ ] Add CI/CD pipeline

## Planned Multi-Agent System

```text
Supervisor Agent
│
├── Source Discovery Agent
├── Web Collection Agent
├── API Collection Agent
├── Document Processing Agent
├── Source Validation Agent
├── Deduplication Agent
├── Relevance Ranking Agent
├── Aptitude Content Agent
├── Communication Content Agent
├── Coding Content Agent
├── Technical Interview Agent
├── HR Interview Agent
├── Assessment Agent
└── Quality Review Agent
```

The exact agent structure will evolve based on real workflow requirements.

## Planned Source Registry

Approved sources will be stored in a registry instead of being hardcoded inside the Source Agent.

```python
APPROVED_SOURCES = {
    "communication": [
        {
            "title": "Approved Grammar Resource",
            "url": "https://example.com/grammar",
            "source_type": "official_documentation",
        }
    ],
    "python": [
        {
            "title": "Python Documentation",
            "url": "https://docs.python.org/3/",
            "source_type": "official_documentation",
        }
    ],
}
```

The Source Agent will use the request domain to select and fetch relevant sources.

## Planned Output Types

- Topic explanations
- Short revision notes
- Detailed study notes
- Multiple-choice questions
- Coding questions
- Aptitude practice sets
- Interview questions
- Mock interviews
- Company-specific preparation plans
- Daily preparation schedules
- Weak-area improvement plans
- Flashcards
- Assessments
- Performance reports

## Example Future Request

```json
{
  "domain": "sql",
  "topic": "joins",
  "requested_output": "interview_questions"
}
```

Expected workflow:

```text
Validate request
      │
      ▼
Select approved SQL sources
      │
      ▼
Collect documentation and examples
      │
      ▼
Clean and normalize content
      │
      ▼
Remove duplicate material
      │
      ▼
Rank relevant sections
      │
      ▼
Generate SQL interview questions
      │
      ▼
Attach source references
      │
      ▼
Return final output
```

## Why Agentic AI?

A traditional application could fetch a website and summarize it. Placement preparation, however, requires several independent decisions:

- Which source should be trusted?
- Which source is relevant to the topic?
- Which content should be removed?
- What output format did the student request?
- Which specialist should handle the request?
- Did the generated material follow the source?
- Should the workflow retry or use another source?

An agentic architecture allows these responsibilities to be separated, tested, monitored, and coordinated.

## Current Limitations

The current version is an early development foundation.

- Only one hardcoded website is fetched.
- Multi-source collection is not implemented.
- Dynamic source discovery is not implemented.
- Source ranking is not implemented.
- Duplicate removal is not implemented.
- Database storage is not implemented.
- LLM-based generation is not implemented.
- The Content Agent currently produces placeholder-style content.
- There is no public API.
- There is no user interface.
- Production security controls are not yet implemented.
- Advanced observability is not yet configured.

## Project Vision

The long-term goal is to create a trusted placement-preparation intelligence system that can:

- Continuously organize placement resources.
- Collect information from approved sources.
- Generate preparation material based on student needs.
- Maintain traceability between content and sources.
- Support multiple placement domains.
- Coordinate specialized agents.
- Evaluate student performance.
- Recommend the next preparation activity.
- Operate as a reusable service for students and institutions.

## Repository

[github.com/Vishal-WD/placement-agent-swarm](https://github.com/Vishal-WD/placement-agent-swarm)

## Author

**Vishal**  
B.Tech Computer Science and Engineering — Data Science

Primary interests:

- Data Engineering
- Agentic AI
- Generative AI
- Retrieval-Augmented Generation
- Multi-agent systems
