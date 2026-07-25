import streamlit as st


def render_employee_profile(profile):

    st.subheader("👤 AI Generated Employee Profile")

    container = st.container(border=True)

    if not profile:

        st.info("Employee profile will appear here after AI processes the resume.")

        st.divider()

        return

    with container:

        col1, col2 = st.columns([1, 5])

        with col1:

            st.image(
                "https://placehold.co/120x120?text=👤",
                width=100
            )

        with col2:

            st.markdown(
                f"""
### {profile.get('first_name', '')} {profile.get('last_name', '')}

**{profile.get('designation', '-') }**

📍 **Location:** {profile.get('location', '-')}

⏳ **Experience:** {profile.get('experience_years', '-')} Years

🏢 **Domain:** {profile.get('department', '-')}
"""
            )

    st.divider()