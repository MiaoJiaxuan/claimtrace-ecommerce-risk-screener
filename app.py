import streamlit as st

from src.rules_baseline import assess_by_rules


st.set_page_config(
    page_title="ClaimTrace",
    page_icon="🔎",
    layout="centered",
)

st.title("ClaimTrace")

st.caption(
    "Evidence-grounded screening for Chinese e-commerce advertising claims"
)

st.info(
    "This prototype provides preliminary screening only. "
    "It does not provide legal advice or automatically approve product copy."
)

claim = st.text_area(
    "Chinese product claim",
    placeholder="例如：本产品是全网销量第一的护肤品。",
    height=120,
)

if st.button("Assess claim", type="primary"):
    if not claim.strip():
        st.warning("Please enter a Chinese product claim.")
    else:
        result = assess_by_rules(claim)

        st.subheader("Rule-based baseline result")

        risk_level = result["risk_level"]

        if risk_level == "high_risk":
            st.error("High risk")
        elif risk_level == "evidence_needed":
            st.warning("Evidence needed")
        elif risk_level == "low_risk":
            st.success("No configured rule was triggered")
        else:
            st.info("Insufficient evidence")

        st.write("**Submitted claim:**")
        st.code(claim)

        st.write("**Matched text:**")
        if result["matched_terms"]:
            st.write(", ".join(result["matched_terms"]))
        else:
            st.write("None")

        st.write("**Reason:**")
        st.write(result["reason"])

        st.write("**Next action:**")
        st.write(result["next_action"])

        st.caption(
            "Method: rules baseline. This result is not a final legal "
            "or platform-compliance decision."
        )