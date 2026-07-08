import pandas as pd
import plotly.express as px
import streamlit as st


def render_top_skills(skills):

    df = pd.DataFrame(skills)

    fig = px.bar(
        df,
        x="employee_count",
        y="skill_name",
        orientation="h",
        text="employee_count",
        title="Top Skills"
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_experience(experience):

    df = pd.DataFrame(experience)

    fig = px.pie(
        df,
        names="experience_range",
        values="employee_count",
        hole=.55,
        title="Experience Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )