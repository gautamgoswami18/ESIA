from app.ai.intent_classifier import IntentClassifier
from app.services.ai_service import AIService
from app.utils.question_parser import QuestionParser
from app.guardrails.guardrail_service import GuardrailService
from app.guardrails.output.output_guard_service import OutputGuardService
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
            state["context"] = intent
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
        state["context"] = result
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
        state["context"] = summary
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
        state["context"] = comparison
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
    
    def guard_node(self, state):

        print(">>> LangGraph : Guard Node")

        result = GuardrailService.validate(
            state["question"]
        )

        if result is None:

            state["guard_passed"] = True
            state["guard_message"] = ""

        else:

            state["guard_passed"] = False
            state["guard_message"] = result.message
            state["answer"] = result.message
            state["content_type"] = "text"

        return state
    
    def guard_failed_node(self, state):

        print(">>> LangGraph : Guard Failed")

        return state
    
    def output_guard_node(self, state):

        print(">>> LangGraph : Output Guard")
        """
        print("=" * 80)
        print(type(state["answer"]))
        print(state["answer"])
        print("=" * 80)
        """
        result = OutputGuardService.validate(
            answer=state["answer"],
            context=state["context"]
        )
    
        if result is not None:
        
            state["output_guard_passed"] = False
            state["output_guard_message"] = result.message
            state["content_type"] = "json"
    
            state["answer"] = {
            
                "query": state["question"],
                "best_candidate": None,
                "other_candidates": [],
                "recommendation": result.message
  
            }
    
            return state
    
        state["output_guard_passed"] = True
        state["output_guard_message"] = ""
    
        state["answer"] = OutputGuardService.sanitize(
            state["answer"]
        )
    
        return state
    
    def output_guard_failed_node(self, state):

        print(">>> Output Guard Failed")

        return state
    