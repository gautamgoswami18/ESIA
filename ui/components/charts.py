import pandas as pd
import plotly.express as px
import streamlit as st


ESIRA_BLUE = "#2563EB"


def render_top_skills(data):

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="employee_count",
        y="skill_name",
        orientation="h",
        text="employee_count",
        color="employee_count",
        color_continuous_scale="Blues",
        title="Top Skills"
    )

    fig.update_layout(

        height=450,

        coloraxis_showscale=False,

        yaxis=dict(
            categoryorder="total ascending"
        ),

        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),

        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_experience(data):

    df = pd.DataFrame(data)

    fig = px.pie(

        df,

        names="experience_range",

        values="employee_count",

        hole=.60,

        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"
    )

    fig.update_layout(

        title="Experience Distribution",

        showlegend=False,

        height=450,

        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )