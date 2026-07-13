import streamlit as st


def render_no_result():

    st.info(
        """
### 🔍 No matching employee found

I couldn't find any employee matching your request.

**Try searching by:**

- **Skill:** Java, Python, React
- **Role:** Backend Developer, AI Engineer
- **Technology:** Spring Boot, Kafka, AWS
"""
    )

    st.markdown("### 💡 Suggested Searches")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("☕ Java Developer", use_container_width=True):
            st.session_state["esira_question"] = "Find Java Developers"
            st.rerun()

    with col2:
        if st.button("🐍 Python Developer", use_container_width=True):
            st.session_state["esira_question"] = "Find Python Developers"
            st.rerun()

    with col3:
        if st.button("⚛️ React Engineer", use_container_width=True):
            st.session_state["esira_question"] = "Find React Developers"
            st.rerun()