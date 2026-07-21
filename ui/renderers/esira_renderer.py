import streamlit as st

from components.candidate_card import render_candidate
from components.recommendation import render_recommendation
from ui.components.no_result import render_no_result


def render(response):

    if response is None:
        st.error("No response received.")
        return

    with st.container():

        st.markdown(
            """
            <div class="assistant-message">
                <div class="assistant-avatar">
                    🤖
                </div>
                <div class="assistant-content">
            """,
            unsafe_allow_html=True
        )

        # -----------------------------
        # SEARCH RESPONSE
        # -----------------------------

        if response.get("intent") == "SEARCH":

            answer = response["answer"]

            best_candidate = answer.get("best_candidate")

            if not best_candidate:
                render_no_result()
            else:

                st.markdown("## 🏆 Best Candidate")

                render_candidate(
                    best_candidate,
                    best=True
                )

                other_candidates = answer.get(
                    "other_candidates",
                    []
                )

                if other_candidates:

                    st.markdown("---")
                    st.markdown("## 👥 Other Candidates")

                    for candidate in other_candidates:

                        render_candidate(candidate)

                recommendation = answer.get(
                    "recommendation"
                )

                if recommendation:

                    st.markdown("---")
                    render_recommendation(
                        recommendation
                    )

        # -----------------------------
        # MARKDOWN
        # -----------------------------

        elif response.get("content_type") == "markdown":

            st.markdown(
                response["answer"]
            )

        # -----------------------------
        # JSON
        # -----------------------------

        elif response.get("content_type") == "json":

            st.json(
                response["answer"]
            )

        # -----------------------------
        # TEXT
        # -----------------------------

        else:

            st.write(
                response["answer"]
            )

        st.markdown(
            """
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )