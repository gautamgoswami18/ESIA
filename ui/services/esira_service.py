from api_client import APIClient


class ESIRAService:

    def __init__(self):
        self.client = APIClient()

    def ask(self, question):

        response = self.client.post(
            "/esira/esiraChat",
            {"question": question}
        )

        return response