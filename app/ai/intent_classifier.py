from app.ai.llm import GeminiLLM


class IntentClassifier:

    def __init__(self):
        self.llm = GeminiLLM.get_llm()

    def classify(
        self,
        question: str
    ) -> str:

        prompt = f"""
You are an AI Intent Classifier.

Classify the user's question into EXACTLY ONE of the following intents.

SEARCH
SUMMARY
COMPARE
SKILL_GAP
TRAINING
INTERVIEW

Rules:

- SEARCH
    Find employees
    Find developer
    Find candidate
    Search resumes

- SUMMARY
    Summarize resume
    Give profile summary
    Tell about employee

- COMPARE
    Compare employee A and B
    Difference between employees

- SKILL_GAP
    Missing skills
    Skill gap
    Ready for role

- TRAINING
    Recommend training
    Learning path
    Upskill

- INTERVIEW
    Generate interview questions
    Prepare interview
    Technical questions

Return ONLY ONE WORD.

Question:

{question}
"""

        response = self.llm.invoke(prompt)

        return(
           response.content
           .strip()
           .replace('"', '')
           .upper()
        )