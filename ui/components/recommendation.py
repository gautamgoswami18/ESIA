import streamlit as st


def render_recommendation(text):

    st.markdown(
        """
        <div class="esira-card">
            <div class="esira-card-title">
                🎯 Recommendation
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(text)

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )