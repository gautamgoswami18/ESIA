import streamlit as st


def render_bulk_upload():

    st.subheader(
        "📂 Bulk Resume Upload"
    )


    files=st.file_uploader(
        "Upload resumes",
        type=["pdf"],
        accept_multiple_files=True
    )


    if files:

        st.success(
            f"{len(files)} resumes uploaded"
        )


        return files