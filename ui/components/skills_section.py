import streamlit as st


def render_skills(skills):

    st.subheader("💻 Technical Skills")

    container = st.container(border=True)

    with container:

        if not skills:

            st.info("No skills extracted.")

            return

        cols = st.columns(4)

        for index, skill in enumerate(skills):

            column = cols[index % 4]

            with column:

                if isinstance(skill, dict):

                    skill_name = (
                        skill.get("name")
                        or skill.get("skill_name")
                        or "-"
                    )

                else:

                    skill_name = getattr(
                        skill,
                        "name",
                        getattr(skill, "skill_name", str(skill))
                    )

                st.success(skill_name)

    st.divider()
