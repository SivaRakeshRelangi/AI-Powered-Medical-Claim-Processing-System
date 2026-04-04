from typing import TypedDict, Annotated
from langgraph.graph import StateGraph

from app.agents.segregator import segregator_agent
from app.agents.id_agent import id_agent
from app.agents.discharge_agent import discharge_agent
from app.agents.bill_agent import bill_agent


# ✅ Define proper state
class GraphState(TypedDict):
    pages: list
    classified_pages: dict

    # Allow parallel updates safely
    id_data: Annotated[dict, "merge"]
    discharge_data: Annotated[dict, "merge"]
    billing_data: Annotated[dict, "merge"]

    final_output: dict


# ✅ Aggregator node
def aggregator(state: GraphState):
    return {
        "final_output": {
            "id": state.get("id_data"),
            "discharge": state.get("discharge_data"),
            "billing": state.get("billing_data"),
        }
    }


# ✅ Build graph
def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("segregator", segregator_agent)
    builder.add_node("id_agent", id_agent)
    builder.add_node("discharge_agent", discharge_agent)
    builder.add_node("bill_agent", bill_agent)
    builder.add_node("aggregator", aggregator)

    # Entry point
    builder.set_entry_point("segregator")

    # Parallel execution
    builder.add_edge("segregator", "id_agent")
    builder.add_edge("segregator", "discharge_agent")
    builder.add_edge("segregator", "bill_agent")

    # Merge into aggregator
    builder.add_edge("id_agent", "aggregator")
    builder.add_edge("discharge_agent", "aggregator")
    builder.add_edge("bill_agent", "aggregator")

    builder.set_finish_point("aggregator")

    return builder.compile()