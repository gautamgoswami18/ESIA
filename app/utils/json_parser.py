import json


class JsonParser:

    @staticmethod
    def parse(response: str):

        if response is None:
            raise Exception("LLM returned empty response.")

        response = response.strip()

        # Remove markdown
        if response.startswith("```json"):
            response = response[7:]

        if response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            return json.loads(response)

        except Exception as ex:

            print("=" * 100)
            print("JSON PARSE ERROR")
            print("=" * 100)
            print(response)
            print("=" * 100)

            raise Exception(
                f"Invalid JSON returned by LLM.\n{ex}"
            )