import json

from app.llm.provider_factory import ProviderFactory
from app.utils.json_parser import JsonParser
from app.ai.prompt import INTENT_PROMPT
from langsmith import traceable
class IntentClassifier:

    def __init__(self):
        self.llm = ProviderFactory.get_provider()
    @traceable(name="Intent Classification")
    def classify(
        self,
        question: str
    ) -> str:

        prompt = INTENT_PROMPT.format(question=question)

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