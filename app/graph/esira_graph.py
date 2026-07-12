from langgraph.graph import StateGraph, END

from app.graph.esira_state import ESIRAState
from app.graph.esira_nodes import ESIRANodes
from app.schemas.esira_schema import ESIRAResponse


class ESIRAGraph:

    def __init__(self, ai_service):

        self.nodes = ESIRANodes(ai_service)

        builder = StateGraph(ESIRAState)

        # Nodes
        builder.add_node("intent", self.nodes.intent_node)
        builder.add_node("search", self.nodes.search_node)
        builder.add_node("summary", self.nodes.summary_node)
        builder.add_node("compare", self.nodes.compare_node)
        builder.add_node("greeting",self.nodes.greeting_node)
        builder.add_node("unknown", self.nodes.unknown_node)
       

        # Entry Point
        builder.set_entry_point("intent")

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
        builder.add_edge("search", END)
        builder.add_edge("summary", END)
        builder.add_edge("compare", END)
        builder.add_edge("greeting", END)
        builder.add_edge("unknown", END)

        self.graph = builder.compile()

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
                "employee2": None
            }
        )

        return ESIRAResponse(
            intent=result["intent"],
            content_type=result["content_type"],
            answer=result["answer"]
        )