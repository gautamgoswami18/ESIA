import streamlit as st


STATUS_ICON = {
    "waiting": "⚪",
    "running": "🟡",
    "completed": "🟢",
    "failed": "🔴"
}


def render_processing_timeline(
    uploaded_file,
    timeline
):

    st.subheader("⚡ Live AI Processing")

    container = st.container(border=True)

    with container:

        if uploaded_file:

            st.markdown(
                f"**📄 Resume:** `{uploaded_file.name}`"
            )

        else:

            st.markdown(
                "**📄 Resume:** _No resume uploaded yet._"
            )

        st.markdown("")

        if any(status == "waiting" for _, status in timeline):
            st.caption(
                "Blue steps are pending and will run after "
                "you click Save Employee."
            )

        for step, status in timeline:

            icon = STATUS_ICON.get(status, "⚪")

            if status == "completed":

                st.success(f"{icon} {step}")

            elif status == "running":

                st.warning(f"{icon} {step}")

            elif status == "failed":

                st.error(f"{icon} {step}")

            else:

                st.info(f"{icon} {step}")

    st.divider()


def render_timeline(status):


    for step,state in status:

        if state=="completed":

            st.success(
                "✔ "+step
            )

        elif state=="processing":

            st.info(
                "⏳ "+step
            )

        else:

            st.write(
                "○ "+step
            )    
