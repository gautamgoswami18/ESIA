import streamlit as st


def render_upload_section():

    st.markdown(
        """
### 📄 Upload Resume

Build your organization's AI knowledge base by uploading employee resumes.
"""
    )

    uploaded_file = st.file_uploader(
        label="Upload Resume",
        type=["pdf"],
        accept_multiple_files=False,
        help="Supports PDF files up to 10 MB",
        label_visibility="collapsed"
    )

    return uploaded_file