import streamlit as st
import requests

st.set_page_config(page_title="AI Invoice Review Agent", page_icon="🧾")

st.title("🧾 AI Invoice Review Agent")
st.write(
    "Upload an invoice PDF and watch three AI agents read it, check it for "
    "hard blockers, score it on softer risk signals, and decide whether to "
    "approve it — all in a few seconds."
)

# This URL points at the local n8n workflow for now — it gets updated
# to a public URL in Week 4 once n8n is deployed online.
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/ff19988e-d6ba-41ef-bc75-9755ff14fa1d"

uploaded_file = st.file_uploader("Upload an invoice PDF", type=["pdf"])

st.caption(
    "Don't have one handy? Try re-uploading any invoice PDF from the "
    "project's /sample-data folder."
)

if uploaded_file and st.button("Process Invoice"):
    with st.spinner("Reading invoice and making a decision..."):
        # files = {"file": uploaded_file}
        # response = requests.post(N8N_WEBHOOK_URL, files=files)
        # result = response.json()
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(N8N_WEBHOOK_URL, files=files)
        result = response.json()

    decision = result.get("decision", "unknown")

    st.divider()
    st.subheader("Final Decision")
    if decision == "approved":
        st.success("✅ **APPROVED** — auto-approved, no review needed")
    elif decision == "escalated_for_review":
        st.warning("⚠️ **ESCALATED** — flagged for human review")
    else:
        st.error("❌ **REJECTED** — needs correction before it can be processed")

    st.divider()
    st.subheader("Tier 1 — Completeness Gate")
    st.caption("Every check below must pass before an invoice is even considered for scoring.")
    tier1_checks = result.get("tier1_checks", [])
    for check in tier1_checks:
        icon = "✅" if check.get("passed") else "❌"
        st.write(f"{icon} {check.get('name')}")

    st.divider()
    st.subheader("Tier 2 — Confidence Score & Findings")
    confidence_score = result.get("confidence_score")
    if confidence_score is not None:
        st.metric("Confidence Score", f"{confidence_score} / 100")
        tier2_findings = result.get("tier2_findings", [])
        if tier2_findings:
            st.write("**Findings:**")
            for finding in tier2_findings:
                st.write(f"- 🔎 {finding}")
        else:
            st.write("No soft-signal concerns found — clean invoice.")
    else:
        st.write("Not applicable — this invoice was rejected at Tier 1 before scoring began.")

    st.divider()
    st.subheader("Extracted Invoice Details")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Vendor:** {result.get('vendor')}")
        st.write(f"**Invoice #:** {result.get('invoice_number')}")
    with col2:
        st.write(f"**Date:** {result.get('date')}")
        st.write(f"**Total:** ${result.get('total')}")

    if result.get("line_items"):
        st.write("**Line Items:**")
        for item in result["line_items"]:
            st.write(
                f"- {item.get('description')}: "
                f"{item.get('quantity')} × ${item.get('unit_price')} = ${item.get('amount')}"
            )

    st.divider()
    st.caption(
        "📋 In production, this decision and the extracted details would be "
        "logged to a company spreadsheet or database for auditing — this demo "
        "keeps that state local to each request rather than persisting it."
    )

    with st.expander("See raw JSON response"):
        st.json(result)