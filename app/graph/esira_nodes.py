from app.ai.intent_classifier import IntentClassifier
from app.services.ai_service import AIService
from app.utils.question_parser import QuestionParser
import traceback

class ESIRANodes:

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.intent_classifier = IntentClassifier()

    def intent_node(self, state):

        print(">>> LangGraph : Intent Node")
        print("State before:", state)
    
        try:
            question = state["question"]
    
            intent = self.intent_classifier.classify(question)
    
            print("Intent =", intent)
    
            state["intent"] = intent
    
            return state
    
        except Exception:
            traceback.print_exc()
            raise

    def search_node(self, state):
        print(">>> LangGraph : Search Node")
        result = self.ai_service.search_resume(
            state["question"]
        )

        state["answer"] = result
        state["content_type"] = "json"

        return state

    def summary_node(self, state):
        print(">>> LangGraph : Summary Node")
        try:
            employee_id = QuestionParser.employee(state["question"])
        except ValueError:
            state["answer"] = "Please provide a valid employee ID."
            state["content_type"] = "text"
            return state
        
        summary = self.ai_service.resume_summary(
            employee_id
        )

        state["employee1"] = employee_id
        state["answer"] = summary
        state["content_type"] = "markdown"

        return state

    def compare_node(self, state):
        print(">>> LangGraph : Compare Node")
        try:
            emp1, emp2 = QuestionParser.employees(state["question"])
        except ValueError:
            state["answer"] = "Please provide a valid employee ID."
            state["content_type"] = "text"
            return state

        comparison = self.ai_service.compare_candidates(
            emp1,
            emp2
        )

        state["employee1"] = emp1
        state["employee2"] = emp2
        state["answer"] = comparison
        state["content_type"] = "markdown"

        return state
    def greeting_node(self, state):

        state["answer"] = (
            "Hello! 👋 I'm ESIA.\n\n"
            "I can help you with:\n"
            "• Find employees\n"
            "• Compare employees\n"
            "• Summarize resumes"
        )

        state["content_type"] = "text"

        return state

    def unknown_node(self, state):

        state["answer"] = "Sorry, I couldn't understand your request."
        state["content_type"] = "text"

        return state