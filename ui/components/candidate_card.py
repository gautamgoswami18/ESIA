import streamlit as st


def render_candidate(candidate, best=False):

    badge = "🏆 Best Match" if best else f"#{candidate['rank']} Candidate"

    with st.container(border=True):

        st.markdown(f"## {badge}")

        st.markdown(f"### {candidate['name']}")

        st.caption(candidate["role"])

        c1, c2 = st.columns(2)

        c1.metric(
            "Experience",
            candidate["experience"]
        )

        c2.metric(
            "Match Score",
            f"{candidate['match_score']}%"
        )

        st.write("### Matching Skills")

        skill_cols = st.columns(
            len(candidate["matching_skills"])
        )

        for i, skill in enumerate(candidate["matching_skills"]):

            skill_cols[i].success(skill)

        st.write("### Why ESIRA Selected")

        st.info(candidate["reason"])