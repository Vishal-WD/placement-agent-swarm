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