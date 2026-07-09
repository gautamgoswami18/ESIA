import streamlit as st

from components.candidate_card import render_candidate
from components.recommendation import render_recommendation


def render(response):

    if "best_candidate" in response:

        st.divider()

        st.subheader("Search Query")

        st.info(response["query"])

        render_candidate(
            response["best_candidate"],
            best=True
        )

        st.divider()

        st.subheader("Other Candidates")

        for candidate in response["other_candidates"]:

            render_candidate(candidate)

        st.divider()

        render_recommendation(
            response["recommendation"]
        )

        return

    st.json(response)