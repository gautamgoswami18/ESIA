import json

from app.llm.provider_factory import ProviderFactory
from app.utils.json_parser import JsonParser

class IntentClassifier:

    def __init__(self):
        self.llm = ProviderFactory.get_provider()

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

Return ONLY valid JSON.

Example:

{{
    "intent": "COMPARE"
}}

Rules:

- Do not explain.
- Do not add extra text.
- Do not use markdown.
- Do not wrap the response in ```json.
- Return only the JSON object.

Question:

{question}
"""

        response = self.llm.generate(
            prompt,
            json_mode=True
        )

        print("=" * 80)
        print("RAW INTENT RESPONSE")
        print(response)
        print("=" * 80)

        try:

            data = JsonParser.parse(response)

            intent = data.get("intent", "").strip().upper()

            if intent == "":
                raise Exception("Intent missing.")

            return intent

        except Exception as ex:

            print("=" * 80)
            print("Intent Parse Error")
            print(ex)
            print("=" * 80)

            raise Exception("Unable to classify intent.")