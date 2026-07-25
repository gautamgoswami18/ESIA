import streamlit as st
import requests


API_URL="http://localhost:8000/resume/save"


def render_save_employee(profile):

    st.subheader("💾 Save Employee")

    if st.button(
        "Save Employee",
        type="primary"
    ):

        response=requests.post(
            API_URL,
            json=profile
        )


        if response.status_code==200:

            st.success(
                "Employee saved successfully"
            )

        else:

            st.error(
                response.text
            )