# Placement Agent Swarm

Placement Agent Swarm is a small LangGraph-based multi-agent workflow project.

The current version demonstrates how multiple agents can work together using a shared state.

At this stage, the project contains three agents:

```text
START
  ↓
Supervisor Agent
  ↓
Source Agent
  ↓
Content Agent
  ↓
END
```

The current logic is intentionally simple.

The project does not yet use an LLM, database, external API, web search, PDF processing, or cloud service.

The purpose of the current version is to build and verify the basic engineering foundation:

- Python project setup
- Isolated environment
- Dependency management
- Shared agent state
- LangGraph workflow
- Agent-to-agent state updates
- Unit tests
- Integration tests
- Linting
- Type checking
- One-command quality validation

---

# 1. Project Location

The project was created at:

```text
D:\Placement-Agent-Swarm
```

All commands in this README are expected to be run from this folder.

Example:

```powershell
cd D:\Placement-Agent-Swarm
```

---

# 2. Tools Verified Before Setup

Before creating the project, the following tools were checked:

```powershell
python --version
git --version
docker --version
code --version
```

The installed versions were:

```text
Python 3.11.15
Git 2.54.0.windows.1
Docker 29.5.3
Visual Studio Code 1.131.0
```

## Why these tools were checked

### Python

Python is the main programming language used for the project.

### Git

Git is used to track code changes and create commits.

### Docker

Docker is installed and available, even though it is not yet used in the current version.

### Visual Studio Code

VS Code is used to edit the project files.

---

# 3. Why `uv` Is Used

The project uses `uv` as the Python environment and dependency manager.

`uv` is responsible for:

- Creating the virtual environment
- Installing packages
- Installing development tools
- Resolving package versions
- Creating the lock file
- Running commands inside the project environment

`uv` was installed with:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

The installation was verified using:

```powershell
uv --version
```

Installed version:

```text
uv 0.12.0
```

## Why not use only `pip`

Using only `pip` would require manually managing:

- The virtual environment
- Runtime dependencies
- Development dependencies
- Exact dependency versions
- Reproducible installation

`uv` handles these tasks in one project workflow.

---

# 4. Project Initialization

The project folder was created using:

```powershell
mkdir D:\Placement-Agent-Swarm
cd D:\Placement-Agent-Swarm
```

The Python project was initialized using:

```powershell
uv init --python 3.11
```

This created the initial files:

```text
.gitignore
.python-version
pyproject.toml
README.md
src/
```

## What `uv init` did

It created a valid Python project structure.

It also created:

### `.python-version`

This records the Python version used by the project.

Current value:

```text
3.11
```

### `pyproject.toml`

This is the main project configuration file.

It stores:

- Project name
- Project version
- Python requirements
- Dependencies
- Development dependencies
- Command-line scripts

### `README.md`

This file documents the project.

### `src/`

This contains the Python source code.

---

# 5. Virtual Environment

The virtual environment was created by running:

```powershell
uv sync
```

This created:

```text
.venv/
uv.lock
```

## Why `.venv` exists

The `.venv` folder contains an isolated Python environment for this project.

It prevents this project's packages from mixing with:

- Global Python packages
- Other projects
- Different package versions

The `.venv` folder should not be committed to Git because it is machine-specific and can be recreated.

## Why `uv.lock` exists

The `uv.lock` file stores the exact resolved package versions.

This makes the environment reproducible.

Another developer can clone the repository and run:

```powershell
uv sync
```

to recreate the same environment.

The lock file should be committed to Git.

---

# 6. Installed Runtime Dependencies

The main dependencies were installed using:

```powershell
uv add langgraph langchain pydantic pydantic-settings python-dotenv
```

## LangGraph

LangGraph is used to create the agent workflow.

It provides:

- Graph nodes
- Graph edges
- Shared state
- Start and end points
- State updates between agents

In this project, each agent is represented as a LangGraph node.

## LangChain

LangChain is installed as a supporting AI framework.

In the current version, it is not directly used by the agent functions.

It is included because the project is being built in the LangChain and LangGraph ecosystem.

## Pydantic

Pydantic is installed for structured data validation.

In the current version, the main graph state uses `TypedDict`, but Pydantic is part of the project dependency foundation.

## Pydantic Settings

This package is installed for application settings and environment-variable handling.

It is not yet used in the current code.

## Python Dotenv

This package is installed for loading values from `.env` files.

It is not yet used in the current code.

---

# 7. Installed Development Dependencies

The development tools were installed using:

```powershell
uv add --dev pytest pytest-cov ruff mypy pre-commit
```

These packages are not required for normal application execution.

They are used to maintain code quality.

## Pytest

Pytest runs automated tests.

It is currently used for:

- Supervisor Agent testing
- Source Agent testing
- Content Agent testing
- Complete graph testing

## Pytest Coverage

Pytest Coverage is installed to measure test coverage.

It is available in the environment, though a coverage percentage is not yet enforced.

## Ruff

Ruff checks the project for:

- Duplicate imports
- Undefined names
- Unused imports
- Import-order problems
- Common Python mistakes

## MyPy

MyPy checks type annotations.

It verifies that:

- Variables have expected types
- Function parameters are correct
- Return values are consistent
- `TypedDict` fields are used properly

## Pre-commit

Pre-commit is installed for Git hook automation.

It is not yet configured in the current version.

---

# 8. Current Project Structure

The current project structure is:

```text
Placement-Agent-Swarm/
│
├── src/
│   └── placement_agent_swarm/
│       ├── __init__.py
│       ├── main.py
│       ├── quality.py
│       │
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── supervisor.py
│       │   ├── source_agent.py
│       │   └── content_agent.py
│       │
│       ├── config/
│       │   └── __init__.py
│       │
│       ├── graphs/
│       │   ├── __init__.py
│       │   └── content_graph.py
│       │
│       └── schemas/
│           ├── __init__.py
│           └── state.py
│
├── tests/
│   ├── __init__.py
│   ├── test_supervisor.py
│   ├── test_source_agent.py
│   ├── test_content_agent.py
│   └── test_content_graph.py
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

---

# 9. Why `__init__.py` Files Exist

The following folders contain `__init__.py` files:

```text
placement_agent_swarm/
agents/
config/
graphs/
schemas/
tests/
```

These files tell Python that the folders should be treated as packages.

This allows imports such as:

```python
from placement_agent_swarm.schemas.state import AgentState
```

Without proper package structure, Python imports may fail.

---

# 10. Shared Agent State

The shared state is defined in:

```text
src/placement_agent_swarm/schemas/state.py
```

Current content:

```python
from enum import StrEnum
from typing import TypedDict


class WorkflowStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentState(TypedDict):
    workflow_id: str
    status: WorkflowStatus
    domain: str
    topic: str
    requested_output: str
    current_agent: str
    next_agent: str
    error_message: str | None
    sources: list[str]
    generated_content: str | None
```

## Why the shared state is needed

The agents need a common data structure.

Without shared state, every agent would need to receive many separate parameters and return unrelated values.

With `AgentState`, every agent receives the same state object and returns only the fields it changes.

This creates a clear data flow.

Example:

```text
Supervisor Agent
    updates status and next agent

Source Agent
    reads topic and adds sources

Content Agent
    reads topic and sources and adds generated content
```

---

# 11. WorkflowStatus

The workflow status is represented using:

```python
class WorkflowStatus(StrEnum):
```

The allowed values are:

```text
created
running
completed
failed
```

## Why `StrEnum` is used

Using an enum prevents random status values such as:

```text
done
finished
complete
success
```

Instead, the code must use one of the defined values.

This makes the workflow more consistent.

## Status meanings

### `CREATED`

The workflow has been created but not started.

### `RUNNING`

The workflow is currently being processed.

### `COMPLETED`

The workflow finished successfully.

### `FAILED`

The workflow failed.

The `FAILED` value is defined but is not yet used by the current agent logic.

---

# 12. AgentState Fields

## `workflow_id`

```python
workflow_id: str
```

This identifies one workflow execution.

Current example:

```text
test-001
```

## `status`

```python
status: WorkflowStatus
```

This stores the current workflow status.

## `domain`

```python
domain: str
```

This stores the content domain.

Current example:

```text
communication
```

## `topic`

```python
topic: str
```

This stores the requested topic.

Current example:

```text
subject-verb agreement
```

## `requested_output`

```python
requested_output: str
```

This stores the requested output type.

Current example:

```text
practice_set
```

## `current_agent`

```python
current_agent: str
```

This stores the most recently executed agent.

## `next_agent`

```python
next_agent: str
```

This stores the next intended agent name.

In the current graph, routing is controlled directly by LangGraph edges.

This field is still useful for visibility and debugging.

## `error_message`

```python
error_message: str | None
```

This stores an error message when one exists.

Current successful workflows keep it as:

```python
None
```

## `sources`

```python
sources: list[str]
```

This stores source values added by the Source Agent.

The current Source Agent adds a placeholder string.

## `generated_content`

```python
generated_content: str | None
```

This stores the content produced by the Content Agent.

Before the Content Agent runs, the value is:

```python
None
```

After it runs, the field contains placeholder content.

---

# 13. Supervisor Agent

The Supervisor Agent is defined in:

```text
src/placement_agent_swarm/agents/supervisor.py
```

Current implementation:

```python
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def supervisor_agent(state: AgentState) -> dict[str, object]:
    return {
        "status": WorkflowStatus.RUNNING,
        "current_agent": "supervisor",
        "next_agent": "source_agent",
        "error_message": None,
    }
```

## What the Supervisor Agent does

It updates:

```text
status → running
current_agent → supervisor
next_agent → source_agent
error_message → None
```

## Why it returns only changed fields

The agent does not return the full state.

It returns only:

```python
{
    "status": ...,
    "current_agent": ...,
    "next_agent": ...,
    "error_message": ...,
}
```

LangGraph merges these returned values into the existing state.

This approach is better because:

- The agent changes only its own fields.
- Existing data remains untouched.
- The function is easier to test.
- State updates are clearer.
- Accidental data overwriting is reduced.

---

# 14. Source Agent

The Source Agent is defined in:

```text
src/placement_agent_swarm/agents/source_agent.py
```

Current implementation:

```python
from placement_agent_swarm.schemas.state import AgentState


def source_agent(state: AgentState) -> dict[str, object]:
    topic = state["topic"]

    return {
        "current_agent": "source_agent",
        "next_agent": "content_agent",
        "sources": [
            f"Approved source placeholder for: {topic}"
        ],
        "error_message": None,
    }
```

## What the Source Agent does

The agent reads:

```python
state["topic"]
```

For the current input:

```text
subject-verb agreement
```

it creates:

```text
Approved source placeholder for: subject-verb agreement
```

It then stores that value in:

```python
sources
```

## Why it uses placeholder logic

The purpose of the current Source Agent is not real source research.

Its purpose is to prove that:

- An agent can read from shared state.
- An agent can create a new value.
- An agent can update the state.
- The next agent can receive that updated value.

---

# 15. Content Agent

The Content Agent is defined in:

```text
src/placement_agent_swarm/agents/content_agent.py
```

Current implementation:

```python
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def content_agent(state: AgentState) -> dict[str, object]:
    topic = state["topic"]
    sources = state["sources"]

    source_summary = ", ".join(sources)

    generated_content = (
        f"Topic: {topic}\n"
        f"Sources: {source_summary}\n"
        "Generated content placeholder."
    )

    return {
        "status": WorkflowStatus.COMPLETED,
        "current_agent": "content_agent",
        "next_agent": "end",
        "generated_content": generated_content,
        "error_message": None,
    }
```

## What the Content Agent reads

It reads:

```python
state["topic"]
state["sources"]
```

This proves that it can use information created by a previous agent.

## What it generates

The current output is similar to:

```text
Topic: subject-verb agreement
Sources: Approved source placeholder for: subject-verb agreement
Generated content placeholder.
```

## What it updates

It sets:

```text
status → completed
current_agent → content_agent
next_agent → end
generated_content → placeholder content
error_message → None
```

---

# 16. LangGraph Workflow

The graph is defined in:

```text
src/placement_agent_swarm/graphs/content_graph.py
```

Current implementation:

```python
from langgraph.graph import END, START, StateGraph

from placement_agent_swarm.agents.content_agent import content_agent
from placement_agent_swarm.agents.source_agent import source_agent
from placement_agent_swarm.agents.supervisor import supervisor_agent
from placement_agent_swarm.schemas.state import AgentState


def build_content_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("source_agent", source_agent)
    graph.add_node("content_agent", content_agent)

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "source_agent")
    graph.add_edge("source_agent", "content_agent")
    graph.add_edge("content_agent", END)

    return graph.compile()
```

## `StateGraph`

```python
graph = StateGraph(AgentState)
```

This creates a graph that uses `AgentState` as its shared state structure.

## `add_node`

```python
graph.add_node("supervisor", supervisor_agent)
```

This registers an agent function as a graph node.

The same process is used for all three agents.

## `add_edge`

```python
graph.add_edge(START, "supervisor")
```

This connects the graph start to the Supervisor Agent.

The full edge order is:

```text
START
  ↓
supervisor
  ↓
source_agent
  ↓
content_agent
  ↓
END
```

## `compile`

```python
return graph.compile()
```

This validates and compiles the graph into an executable workflow.

---

# 17. Main Runner

The workflow runner is defined in:

```text
src/placement_agent_swarm/main.py
```

Current implementation:

```python
from placement_agent_swarm.graphs.content_graph import build_content_graph
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def main() -> None:
    graph = build_content_graph()

    initial_state: AgentState = {
        "workflow_id": "test-001",
        "status": WorkflowStatus.CREATED,
        "domain": "communication",
        "topic": "subject-verb agreement",
        "requested_output": "practice_set",
        "current_agent": "",
        "next_agent": "",
        "error_message": None,
        "sources": [],
        "generated_content": None,
    }

    result = graph.invoke(initial_state)
    print(result)


if __name__ == "__main__":
    main()
```

## Why `initial_state` is typed

It is defined as:

```python
initial_state: AgentState
```

This allows MyPy to check whether all required state fields are present and correctly typed.

## Why `graph.invoke()` is used

```python
result = graph.invoke(initial_state)
```

This sends the initial state into the graph.

LangGraph then executes each connected node.

The final merged state is returned as `result`.

## How to run the workflow

```powershell
uv run python -m placement_agent_swarm.main
```

Current output:

```text
{
    'workflow_id': 'test-001',
    'status': <WorkflowStatus.COMPLETED: 'completed'>,
    'domain': 'communication',
    'topic': 'subject-verb agreement',
    'requested_output': 'practice_set',
    'current_agent': 'content_agent',
    'next_agent': 'end',
    'error_message': None,
    'sources': [
        'Approved source placeholder for: subject-verb agreement'
    ],
    'generated_content': 'Topic: subject-verb agreement...'
}
```

---

# 18. Automated Tests

The project currently contains four tests.

The tests are stored in:

```text
tests/
```

Testing is important because a change in one agent can affect the full workflow.

---

# 19. Supervisor Agent Test

File:

```text
tests/test_supervisor.py
```

This test verifies that:

- The workflow status becomes `RUNNING`.
- The current agent becomes `supervisor`.
- The next agent becomes `source_agent`.
- The original input state remains unchanged.

The last check confirms that the agent returns state updates instead of modifying the original dictionary directly.

---

# 20. Source Agent Test

File:

```text
tests/test_source_agent.py
```

This test verifies that:

- The agent reads the topic.
- The source placeholder contains the topic.
- The current agent becomes `source_agent`.
- The next agent becomes `content_agent`.
- No error message is returned.

---

# 21. Content Agent Test

File:

```text
tests/test_content_agent.py
```

This test verifies that:

- The workflow status becomes `COMPLETED`.
- The current agent becomes `content_agent`.
- The next agent becomes `end`.
- Generated content is not empty.
- The generated content contains the requested topic.

---

# 22. Full Graph Test

File:

```text
tests/test_content_graph.py
```

This test runs the entire graph:

```text
Supervisor Agent
        ↓
Source Agent
        ↓
Content Agent
```

It verifies the final state after all agents complete.

The test checks:

- Final workflow status
- Final current agent
- Final next-agent value
- Source placeholder
- Generated content
- Topic preservation

---

# 23. Running Tests

Run all tests using:

```powershell
uv run pytest -v
```

Current result:

```text
4 passed
```

The tested files are:

```text
test_supervisor.py
test_source_agent.py
test_content_agent.py
test_content_graph.py
```

---

# 24. Ruff Code Quality Check

Ruff is run using:

```powershell
uv run ruff check .
```

Current result:

```text
All checks passed!
```

## Problems Ruff found during development

### Duplicate import

The Content Agent temporarily contained:

```python
from placement_agent_swarm.schemas.state import AgentState
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus
```

Ruff identified:

- Unsorted imports
- Duplicate `AgentState` definition

It was corrected to:

```python
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus
```

### Undefined function name

The Content Agent test temporarily called:

```python
content_agent(state)
```

without importing `content_agent`.

Ruff reported:

```text
Undefined name `content_agent`
```

It was fixed by adding:

```python
from placement_agent_swarm.agents.content_agent import content_agent
```

---

# 25. MyPy Type Checking

MyPy is run using:

```powershell
uv run mypy src
```

Current result:

```text
Success: no issues found in 12 source files
```

## Problem MyPy found during development

The initial state in `main.py` was first written without a type annotation:

```python
initial_state = {
```

MyPy reported:

```text
Need type annotation for "initial_state"
```

It was corrected to:

```python
initial_state: AgentState = {
```

This lets MyPy validate the state structure.

---

# 26. Single Quality-Check Command

The project includes:

```text
src/placement_agent_swarm/quality.py
```

Current implementation:

```python
import subprocess
import sys


def run_command(command: list[str]) -> int:
    result = subprocess.run(command, check=False)
    return result.returncode


def main() -> None:
    commands = [
        ["ruff", "check", "."],
        ["mypy", "src"],
        ["pytest", "-v"],
    ]

    for command in commands:
        exit_code = run_command(command)

        if exit_code != 0:
            sys.exit(exit_code)

    print("All quality checks passed.")


if __name__ == "__main__":
    main()
```

## What this script does

It runs:

```text
Ruff
MyPy
Pytest
```

in that order.

If one command fails, the script exits immediately with the same failure code.

This prevents tests from appearing successful when linting or type checking has failed.

## Registered command

The command is registered in `pyproject.toml`:

```toml
[project.scripts]
quality-check = "placement_agent_swarm.quality:main"
```

## Run all checks

```powershell
uv run quality-check
```

Current successful output includes:

```text
All checks passed!
Success: no issues found in 12 source files
4 passed
All quality checks passed.
```

---

# 27. Problems Solved During Setup

## Large `tree /F` output

Running:

```powershell
tree /F
```

printed every file inside `.venv`.

This happened because `.venv` contains all installed Python packages.

Nothing was wrong with the project.

To inspect only source code, use:

```powershell
tree src /F
```

To inspect only tests, use:

```powershell
tree tests /F
```

---

## Windows `tree` accepted only one path

This command failed:

```powershell
tree src tests
```

with:

```text
Too many parameters
```

Windows `tree` accepts one path at a time.

The correct usage is:

```powershell
tree src
tree tests
```

---

## No output from `py_compile`

Commands such as:

```powershell
uv run python -m py_compile src\placement_agent_swarm\schemas\state.py
```

showed no output.

This means compilation succeeded.

`py_compile` displays output only when a syntax error occurs.

---

## Indentation error in a test

The test file temporarily produced:

```text
IndentationError: unexpected indent
```

This happened because one `assert` statement had extra indentation.

The fix was to align all assertions at the same indentation level inside the test function.

---

## Test expectation changed after adding Content Agent

Before the Content Agent was connected, the graph ended at:

```text
source_agent
```

After the Content Agent was added, the final current agent became:

```text
content_agent
```

The integration test initially still expected:

```text
source_agent
```

The test was updated to match the new completed graph.

---

## Duplicate `[project.scripts]` section

A second section named:

```toml
[project.scripts]
```

was added to `pyproject.toml`.

TOML does not allow the same table to be declared twice.

This caused:

```text
duplicate key
```

The fix was to keep one section and place both commands inside it.

---

## `uv` hardlink warning

During package installation, `uv` displayed:

```text
Failed to hardlink files; falling back to full copy
```

This happened because the `uv` cache and the project environment were on different filesystems or drives.

The installation still completed successfully.

The warning only indicates that files were copied instead of hardlinked.

---

# 28. Current Verified Status

The current project status is:

```text
Python project initialized
Virtual environment created
Dependencies installed
Shared AgentState created
Supervisor Agent working
Source Agent working with placeholder logic
Content Agent working with placeholder logic
LangGraph workflow working
Main runner working
Four automated tests passing
Ruff checks passing
MyPy checks passing
Single quality-check command working
```

---

# 29. Commands Used So Far

## Check tools

```powershell
python --version
git --version
docker --version
code --version
```

## Install `uv`

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Verify `uv`

```powershell
uv --version
```

## Create project

```powershell
mkdir D:\Placement-Agent-Swarm
cd D:\Placement-Agent-Swarm
uv init --python 3.11
```

## Create environment

```powershell
uv sync
```

## Install runtime dependencies

```powershell
uv add langgraph langchain pydantic pydantic-settings python-dotenv
```

## Install development dependencies

```powershell
uv add --dev pytest pytest-cov ruff mypy pre-commit
```

## Open project

```powershell
code .
```

## Run workflow

```powershell
uv run python -m placement_agent_swarm.main
```

## Run tests

```powershell
uv run pytest -v
```

## Run Ruff

```powershell
uv run ruff check .
```

## Run MyPy

```powershell
uv run mypy src
```

## Run all quality checks

```powershell
uv run quality-check
```

---

# 30. Commit Preparation

Before creating the first stable commit, run:

```powershell
uv run quality-check
```

The expected result is:

```text
Ruff passed
MyPy passed
4 tests passed
All quality checks passed
```

Then check the files:

```powershell
git status
```

Stage them:

```powershell
git add .
```

Create the commit:

```powershell
git commit -m "Set up initial LangGraph agent workflow"
```

This commit represents the completed project foundation documented in this README.