from app.ai.intent_classifier import IntentClassifier
from app.services.ai_service import AIService


class ESIRAService:

    def __init__(self, db):

        self.db = db
        self.intent_classifier = IntentClassifier()
        self.ai_service = AIService(db)

    def ask(self, question: str):

        intent = self.intent_classifier.classify(question)
        print("Intent =", intent)
        print("repr =", repr(intent))
        if intent == "SEARCH":

            return self.ai_service.search_resume(question)

        elif intent == "SUMMARY":

            employee_id = self._extract_employee_id(question)
            print("Employee ID:", employee_id)

            return self.ai_service.resume_summary(employee_id)

        elif intent == "COMPARE":

            emp1, emp2 = self._extract_two_employee_ids(question)

            return self.ai_service.compare_candidates(emp1, emp2)

        else:

            return {
                "assistant": "ESIRA",
                "intent": intent,
                "answer": "Sorry, I couldn't understand your request."
            }

    def _extract_employee_id(self, question):

        import re

        match = re.search(r"\d+", question)

        if match:
            return int(match.group())

        raise Exception("Employee id not found.")

    def _extract_two_employee_ids(self, question):

        import re

        ids = re.findall(r"\d+", question)

        if len(ids) >= 2:
            return int(ids[0]), int(ids[1])

        raise Exception("Two employee ids required.")