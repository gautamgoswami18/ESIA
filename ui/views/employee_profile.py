import streamlit as st

from services.employee_service import EmployeeService

service = EmployeeService()


def show_employee_profile(employee_id):

    profile = service.get_employee_profile(employee_id)

    employee = profile["employee"]

    st.button(
        "← Back",
        on_click=lambda: st.session_state.update(
            {
                "selected_employee": None
            }
        )
    )

    st.title(
        f"👤 {employee['first_name']} {employee['last_name']}"
    )

    st.caption(employee["designation"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Location", employee["location"])

    c2.metric(
        "Experience",
        employee["experience_years"]
    )

    c3.metric(
        "Primary Skill",
        employee["primary_skill"]
    )

    c4.metric(
        "Availability",
        employee["availability"]
    )

    st.divider()

    tabs = st.tabs(
        [
            "Overview",
            "Skills",
            "Projects",
            "Certifications",
            "Resume",
            "AI Summary"
        ]
    )

    with tabs[0]:

        
        st.subheader("Employee Information")
    
        col1, col2 = st.columns(2)
    
        with col1:
        
            st.text_input("First Name", employee["first_name"], disabled=True)
            st.text_input("Last Name", employee["last_name"], disabled=True)
            st.text_input("Designation", employee["designation"], disabled=True)
            st.text_input("Email", employee["email"], disabled=True)
            st.text_input("Location", employee["location"], disabled=True)
            st.text_input("Domain", employee["domain"], disabled=True)
    
        with col2:
        
            st.text_input("Experience", f'{employee["experience_years"]} Years', disabled=True)
            st.text_input("Primary Skill", employee["primary_skill"], disabled=True)
            st.text_input("Utilization", f'{employee["utilization"]}%', disabled=True)
            st.text_input("Availability", employee["availability"], disabled=True)
            st.text_input("Joining Date", employee["joining_date"], disabled=True)
            st.text_input("Status", employee["employment_status"], disabled=True)

    with tabs[1]:

        st.dataframe(
            profile["skills"],
            use_container_width=True,
            hide_index=True
        )

    with tabs[2]:

        st.dataframe(
            profile["projects"],
            use_container_width=True,
            hide_index=True
        )

    with tabs[3]:

        st.dataframe(
            profile["certifications"],
            use_container_width=True,
            hide_index=True
        )

    with tabs[4]:

        resume_file = profile["resume"]["file_name"]

        resume_path = profile["resume"]["file_path"]
    
        col1, col2 = st.columns([5, 1])
    
        with col1:
            st.info(resume_file)
    
        with col2:
            with open(resume_path, "rb") as file:
                st.download_button(
                    label="⬇ Download",
                    data=file,
                    file_name=resume_file,
                    mime="application/pdf",
                    use_container_width=True
                )

    with tabs[5]:

        st.write(profile["summary"])