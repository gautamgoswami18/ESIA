import requests

from config import API_BASE_URL


class APIClient:

    def get(self, endpoint: str):

        response = requests.get(
            f"{API_BASE_URL}{endpoint}"
        )

        response.raise_for_status()

        return response.json()


    def post(
        self,
        endpoint: str,
        payload: dict
    ):

        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload
        )

        response.raise_for_status()

        return response.json()