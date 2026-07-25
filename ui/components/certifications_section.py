import streamlit as st


def render_certifications(certifications):

    st.subheader("🏆 Certifications")

    container = st.container(border=True)

    with container:

        if not certifications:

            st.info("No certifications extracted.")

            st.divider()

            return

        cols = st.columns(2)

        for index, certification in enumerate(certifications):

            column = cols[index % 2]

            with column:

                if isinstance(certification, dict):

                    name = certification.get(
                        "name"
                    ) or certification.get(
                        "certification_name"
                    ) or "-"

                    vendor = certification.get(
                        "issuing_organization"
                    ) or certification.get(
                        "vendor"
                    ) or "-"

                    issue_date = certification.get(
                        "issue_date",
                        "-"
                    ) or "-"

                    status = certification.get(
                        "certification_status"
                    ) or (
                        "Valid"
                        if not certification.get("expiry_date")
                        else f"Expires {certification['expiry_date']}"
                    )

                else:

                    name = getattr(
                        certification,
                        "name",
                        getattr(certification, "certification_name", "-")
                    )

                    vendor = getattr(
                        certification,
                        "issuing_organization",
                        getattr(certification, "vendor", "-")
                    )

                    issue_date = getattr(
                        certification,
                        "issue_date",
                        "-"
                    ) or "-"

                    status = getattr(
                        certification,
                        "certification_status",
                        None
                    ) or (
                        "Valid"
                        if not getattr(certification, "expiry_date", None)
                        else f"Expires {certification.expiry_date}"
                    )

                with st.container(border=True):

                    st.markdown(f"### 🏅 {name}")

                    st.write(f"**Vendor:** {vendor}")

                    st.write(f"**Issued:** {issue_date}")

                    st.write(f"**Status:** {status}")

    st.divider()
