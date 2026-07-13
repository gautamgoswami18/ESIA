from langgraph.graph import StateGraph, END

from app.graph.esira_state import ESIRAState
from app.graph.esira_nodes import ESIRANodes
from app.schemas.esira_schema import ESIRAResponse


class ESIRAGraph:

    def __init__(self, ai_service):

        self.nodes = ESIRANodes(ai_service)

        builder = StateGraph(ESIRAState)

        # Nodes
        builder.add_node("guard", self.nodes.guard_node)
        builder.add_node("intent", self.nodes.intent_node)
        builder.add_node("search", self.nodes.search_node)
        builder.add_node("summary", self.nodes.summary_node)
        builder.add_node("compare", self.nodes.compare_node)
        builder.add_node("greeting",self.nodes.greeting_node)
        builder.add_node("unknown", self.nodes.unknown_node)
        builder.add_node("guard_failed", self.nodes.guard_failed_node)
        builder.add_node("output_guard", self.nodes.output_guard_node)
        builder.add_node("output_guard_failed",self.nodes.output_guard_failed_node)
        

        # Entry Point
        #builder.set_entry_point("intent")
        builder.set_entry_point("guard")
        # Routing
        builder.add_conditional_edges(
            "intent",
            self.route,
            {
                "SEARCH": "search",
                "SUMMARY": "summary",
                "COMPARE": "compare",
                "GREETING":"greeting",
                "UNKNOWN": "unknown"
            }
        )

        # End Nodes
        builder.add_edge("search", "output_guard")
        builder.add_edge("summary", "output_guard")
        builder.add_edge("compare", "output_guard")
        builder.add_edge("greeting", "output_guard")
        builder.add_edge("unknown", "output_guard")
        builder.add_edge("guard_failed", "output_guard")
        builder.add_conditional_edges(
            "guard",
            self.guard_route,
            {
                "PASS": "intent",
                "FAIL": "guard_failed"
            }
        )
        builder.add_conditional_edges(
            "output_guard",
            self.output_guard_route,
            {
                "PASS": END,
                "FAIL": "output_guard_failed"
            }
        )
        self.graph = builder.compile()
    def guard_route(
        self,
        state
    ):

        if state["guard_passed"]:
            return "PASS"

        return "FAIL"
    def route(
        self,
        state: ESIRAState
    ):
        intent = state["intent"]

        if intent == "SEARCH":
            return "SEARCH"

        elif intent == "SUMMARY":
            return "SUMMARY"

        elif intent == "COMPARE":
            return "COMPARE"
        
        elif intent == "GREETING":
            return "GREETING"

        return "UNKNOWN"
    def output_guard_route(
        self,
        state
    ):

        if state["output_guard_passed"]:
            return "PASS"

        return "FAIL"

    def invoke(
        self,
        question: str
    ) -> ESIRAResponse:

        result = self.graph.invoke(
            {
                "question": question,
                "intent": "",
                "answer": None,
                "content_type": "",
                "employee1": None,
                "employee2": None,
                "guard_passed": True,
                "guard_message": ""
            }
        )

        return ESIRAResponse(
            intent=result["intent"],
            content_type=result["content_type"],
            answer=result["answer"]
        )