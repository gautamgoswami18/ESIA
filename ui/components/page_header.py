import streamlit as st


def render_page_header():

    left, right = st.columns([8, 2])

    with left:

        st.title("🧠 AI Knowledge Studio")

        st.caption(
            "Build your organization's AI knowledge base by uploading employee resumes."
        )

    with right:

        st.button(
            "📂 Bulk Upload",
            use_container_width=True
        )

    st.divider()