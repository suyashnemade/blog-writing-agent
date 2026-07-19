
from langgraph.graph import StateGraph, END, START
from blogwriter.states import State
from blogwriter.agents.router import router_node
from blogwriter.agents.research import research_node
from blogwriter.agents.orchestrator import orchestrator_node
from blogwriter.agents.worker import worker_node
from blogwriter.agents.reducer import reducer_subgraph

from blogwriter.routing import route_next
from blogwriter.routing import fanout

g = StateGraph(State)
g.add_node("router", router_node)
g.add_node("research", research_node)
g.add_node("orchestrator", orchestrator_node)
g.add_node("worker", worker_node)
g.add_node("reducer", reducer_subgraph)

g.add_edge(START, "router")
g.add_conditional_edges("router", route_next, {"research": "research", "orchestrator": "orchestrator"})
g.add_edge("research", "orchestrator")

g.add_conditional_edges("orchestrator", fanout, ["worker"])
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()



