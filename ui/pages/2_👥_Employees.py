import streamlit as st

from services.employee_service import EmployeeService
from components.employee_card import render_employee_card
from views.employee_profile import show_employee_profile

service = EmployeeService()

if "selected_employee" not in st.session_state:

    st.session_state.selected_employee = None

if st.session_state.selected_employee:

    show_employee_profile(
        st.session_state.selected_employee
    )

else:

    st.title("👥 Employees")

    employees = service.get_employees()

    for emp in employees:

        render_employee_card(emp)