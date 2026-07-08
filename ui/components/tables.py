import pandas as pd
import streamlit as st


def render_certifications(data):

    st.subheader("🏆 Top Certifications")

    df = pd.DataFrame(data)

    df.columns = [
        "Certification",
        "Employees"
    ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )