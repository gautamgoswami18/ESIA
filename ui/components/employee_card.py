import streamlit as st


def render_employee_card(emp):

    with st.container(border=True):

        left, right = st.columns([5, 1])

        with left:

            st.subheader(
                f"{emp['first_name']} {emp['last_name']}"
            )

            st.caption(emp["designation"])

            st.write(
                f"🛠 {emp['primary_skill']}"
            )

            st.write(
                f"📍 {emp['location']}"
            )

            st.write(
                f"⭐ {emp['experience_years']} Years"
            )

        with right:

            if st.button(
                "View Profile",
                key=emp["employee_id"]
            ):

                st.session_state.selected_employee = emp["employee_id"]

                st.rerun()