import pandas as pd
import streamlit as st


def render_certifications(data):

    st.subheader("🏆 Top Certifications")

    df = pd.DataFrame(data)

    df.insert(
        0,
        "Rank",
        [
            "🥇",
            "🥈",
            "🥉",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10"
        ]
    )

    df.columns = [

        "Rank",

        "Certification",

        "Employees"

    ]

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True
    )