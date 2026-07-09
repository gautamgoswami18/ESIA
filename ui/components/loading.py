import streamlit as st


class Loading:

    @staticmethod
    def show(message="Loading Dashboard..."):

        return st.spinner(message)