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

        skills = candidate.get("matching_skills") or []

        if len(skills) > 0:
        
            cols = st.columns(min(len(skills), 4))
        
            for index, skill in enumerate(skills):
                cols[index % len(cols)].success(skill)
        
        else:
        
            st.info("No matching skills")