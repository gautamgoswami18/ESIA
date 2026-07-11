import streamlit as st

from components.candidate_card  import render_candidate
from components.recommendation import render_recommendation


def render(response):

    if response is None:
        st.error("No response received.")
        return

    # Search Response
    if response.get("intent") == "SEARCH":

        answer = response["answer"]

        st.divider()
        st.subheader("Search Query")
        st.info(answer["query"])

        render_candidate(
            answer["best_candidate"],
            best=True
        )

        st.divider()
        st.subheader("Other Candidates")

        for candidate in answer.get("other_candidates", []):
            render_candidate(candidate)

        if answer.get("recommendation"):
            st.divider()
            render_recommendation(
                answer["recommendation"]
            )

        return

    # Markdown Response
    elif response.get("content_type") == "markdown":

        st.markdown(response["answer"])

    # JSON Response
    elif response.get("content_type") == "json":

        st.json(response["answer"])

    # Text Response
    else:

        st.write(response["answer"])