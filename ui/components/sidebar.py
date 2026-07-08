import streamlit as st

from streamlit_option_menu import option_menu


def render_sidebar():

    with st.sidebar:

        st.image(
            "assets/logo.png",
            width=120
        )

        selected = option_menu(

            menu_title="Navigation",

            options=[
                "Dashboard",
                "Employees",
                "ESIRA"
            ],

            icons=[
                "speedometer2",
                "people",
                "robot"
            ],

            default_index=0

        )

    return selected