import streamlit as st


def render_projects(projects):

    st.subheader("📂 Projects")

    container = st.container(border=True)

    with container:

        if not projects:

            st.info("No projects extracted.")

            st.divider()

            return

        for project in projects:

            if isinstance(project, dict):

                project_name = (
                    project.get("name")
                    or project.get("project_name")
                    or "-"
                )
                client_name = (
                    project.get("client")
                    or project.get("client_name")
                    or "-"
                )
                role_name = (
                    project.get("role")
                    or project.get("role_name")
                    or "-"
                )
                domain = project.get("domain") or "-"

            else:

                project_name = getattr(
                    project,
                    "name",
                    getattr(project, "project_name", "-")
                )
                client_name = getattr(
                    project,
                    "client",
                    getattr(project, "client_name", "-")
                )
                role_name = getattr(
                    project,
                    "role",
                    getattr(project, "role_name", "-")
                )
                domain = getattr(project, "domain", "-")

            with st.container(border=True):

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(f"### {project_name}")

                    st.write(f"**Client :** {client_name}")

                with col2:

                    st.write(f"**Role :** {role_name}")

                    st.write(f"**Domain :** {domain}")

                description = (
                    project.get("description")
                    if isinstance(project, dict)
                    else getattr(project, "description", None)
                )
                technologies = (
                    project.get("technologies", [])
                    if isinstance(project, dict)
                    else getattr(project, "technologies", [])
                )
                responsibilities = (
                    project.get("responsibilities", [])
                    if isinstance(project, dict)
                    else getattr(project, "responsibilities", [])
                )

                if description:
                    st.write(f"**Description:** {description}")

                if technologies:
                    st.write(
                        "**Technologies:** "
                        + ", ".join(technologies)
                    )

                if responsibilities:
                    st.write("**Responsibilities:**")
                    for responsibility in responsibilities:
                        st.write(f"- {responsibility}")

    st.divider()
