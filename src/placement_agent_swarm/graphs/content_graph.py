from typing import Literal

from langgraph.graph import END, START, StateGraph

from placement_agent_swarm.agents.content_agent import content_agent
from placement_agent_swarm.agents.source_agent import source_agent
from placement_agent_swarm.agents.supervisor import supervisor_agent
from placement_agent_swarm.schemas.state import AgentState, WorkflowStatus


def route_after_source(
    state: AgentState,
) -> Literal["content_agent", "end"]:
    if state.status == WorkflowStatus.FAILED:
        return "end"

    return "content_agent"


def build_content_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("source_agent", source_agent)
    graph.add_node("content_agent", content_agent)

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "source_agent")

    graph.add_conditional_edges(
        "source_agent",
        route_after_source,
        {
            "content_agent": "content_agent",
            "end": END,
        },
    )

    graph.add_edge("content_agent", END)

    return graph.compile()