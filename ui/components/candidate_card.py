import streamlit as st


def render_candidate(candidate, best=False):

    badge = "🏆 Best Match" if best else f"#{candidate['rank']} Candidate"

    with st.container(border=True):

        st.markdown(f"### {badge}")

        st.markdown(f"## {candidate['name']}")

        st.caption(candidate["role"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Experience",
                candidate["experience"]
            )

        with col2:
            st.metric(
                "Match Score",
                f"{candidate['match_score']}%"
            )

        st.divider()

        st.markdown("#### ✅ Matching Skills")

        skills = candidate.get("matching_skills", [])

        if skills:

            skill_cols = st.columns(4)

            for i, skill in enumerate(skills):
                with skill_cols[i % 4]:
                    st.success(skill)

        else:
            st.info("No matching skills found.")

        # Optional Details

        location = candidate.get("location")
        domain = candidate.get("domain")
        availability = candidate.get("availability")

        if location or domain or availability:

            st.divider()

            info1, info2, info3 = st.columns(3)

            with info1:
                if location:
                    st.caption("📍 Location")
                    st.write(location)

            with info2:
                if domain:
                    st.caption("💼 Domain")
                    st.write(domain)

            with info3:
                if availability:
                    st.caption("🟢 Availability")
                    st.write(availability)