from app.ai.intent_classifier import IntentClassifier
from app.schemas.esira_schema import ESIRAResponse
from app.services.ai_service import AIService
from app.utils.question_parser import QuestionParser


class ESIRAService:

    def __init__(self, db):
        self.db = db
        self.intent_classifier = IntentClassifier()
        self.ai_service = AIService(db)

    def ask(
        self,
        question: str
    ) -> ESIRAResponse:

        intent = self.intent_classifier.classify(question)

        print("=" * 80)
        print("Intent :", intent)
        print("=" * 80)

        try:

            if intent == "SEARCH":

                result = self.ai_service.search_resume(question)

                return ESIRAResponse(
                    intent="SEARCH",
                    content_type="json",
                    answer=result
                )

            elif intent == "SUMMARY":

                employee_id = QuestionParser.employee(question)

                summary = self.ai_service.resume_summary(
                    employee_id
                )

                return ESIRAResponse(
                    intent="SUMMARY",
                    content_type="markdown",
                    answer=summary
                )

            elif intent == "COMPARE":

                emp1, emp2 = QuestionParser.employees(question)

                comparison = self.ai_service.compare_candidates(
                    emp1,
                    emp2
                )

                return ESIRAResponse(
                    intent="COMPARE",
                    content_type="markdown",
                    answer=comparison
                )
                # will implement below code in V2
                """
                elif intent == "SKILL_GAP":

                    employee_id = QuestionParser.employee(question)

                    result = self.ai_service.skill_gap(employee_id)

                    return ESIRAResponse(
                        intent="SKILL_GAP",
                        content_type="json",
                        answer=result
                    )

                elif intent == "TRAINING":

                    employee_id = QuestionParser.employee(question)

                    result = self.ai_service.training_recommendation(
                        employee_id
                    )

                    return ESIRAResponse(
                        intent="TRAINING",
                        content_type="json",
                        answer=result
                    )

                elif intent == "INTERVIEW":

                    employee_id = QuestionParser.employee(question)

                    result = self.ai_service.interview_questions(
                        employee_id
                    )

                    return ESIRAResponse(
                        intent="INTERVIEW",
                        content_type="markdown",
                        answer=result
                    )
                    """
            else:

                return ESIRAResponse(
                    intent="UNKNOWN",
                    content_type="text",
                    answer="Sorry, I couldn't understand your request."
                )

        except Exception as ex:

            return ESIRAResponse(
                intent="ERROR",
                content_type="text",
                answer=str(ex)
            )