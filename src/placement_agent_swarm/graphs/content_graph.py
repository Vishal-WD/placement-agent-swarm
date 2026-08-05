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