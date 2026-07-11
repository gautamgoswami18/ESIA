import requests
import streamlit as st

from config import API_BASE_URL


class APIClient:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def get(
    self,
    endpoint: str,
    params: dict | None = None
    ):
    
        try:
        
            response = self.session.get(
                f"{API_BASE_URL}{endpoint}",
                params=params,
                timeout=100
            )
    
            response.raise_for_status()
    
            return response.json()
    
        except requests.exceptions.RequestException as ex:
        
            st.error(f"Unable to connect to ESIA Backend.\n\n{ex}")
            st.stop()

    def post(
        self,
        endpoint: str,
        payload: dict
    ):

        try:

            response = self.session.post(
                f"{API_BASE_URL}{endpoint}",
                json=payload,
                timeout=180
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as ex:

            st.error(f"Unable to connect to ESIA Backend.\n\n{ex}")

            st.stop()