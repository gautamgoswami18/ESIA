import streamlit as st


def render_action_buttons():

    st.subheader("💾 Save Employee")

    col1, col2, col3 = st.columns([2, 2, 6])

    with col1:

        save_clicked = st.button(
            "💾 Save Employee",
            type="primary",
            use_container_width=True
        )

    with col2:

        clear_clicked = st.button(
            "🗑 Clear",
            use_container_width=True
        )

    return save_clicked, clear_clicked

