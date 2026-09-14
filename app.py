import streamlit as st

from src.risk_pipeline import ClaimTracePipeline
from src.rules_baseline import assess_by_rules


st.set_page_config(
    page_title="ClaimTrace",
    page_icon="🔎",
    layout="centered",
)


@st.cache_resource(show_spinner="Loading the multilingual retrieval model...")
def load_pipeline() -> ClaimTracePipeline:
    """Load the retrieval model once and reuse it."""
    return ClaimTracePipeline()


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
        baseline_result = assess_by_rules(claim)

        st.subheader("1. Rule-based baseline")

        risk_level = baseline_result["risk_level"]

        if risk_level == "high_risk":
            st.error("High risk")
        elif risk_level == "evidence_needed":
            st.warning("Evidence needed")
        elif risk_level == "low_risk":
            st.success("No configured rule was triggered")
        else:
            st.info("Insufficient evidence")

        st.write("**Matched text:**")

        if baseline_result["matched_terms"]:
            st.write(", ".join(baseline_result["matched_terms"]))
        else:
            st.write("None")

        st.write("**Reason:**")
        st.write(baseline_result["reason"])

        st.divider()
        st.subheader("2. Retrieved evidence")

        with st.spinner("Searching the fixed official-case corpus..."):
            pipeline = load_pipeline()
            retrieval_result = pipeline.retrieve_evidence(claim)

        if retrieval_result["abstain"]:
            st.warning("Insufficient evidence — human review required.")
        else:
            st.success("Relevant evidence found.")

        st.write(
            f"Top similarity score: "
            f"{retrieval_result['top_score']:.4f}"
        )

        st.caption(
            "The current threshold of 0.30 is provisional and will be "
            "calibrated using the development set."
        )

        for case in retrieval_result["retrieved_cases"]:
            heading = (
                f"{case['case_id']} — {case['title']} "
                f"(score: {case['similarity_score']:.4f})"
            )

            with st.expander(heading):
                st.write(case["case_text"])
                st.write(f"Risk type: `{case['risk_type']}`")
                st.markdown(
                    f"[Open the official source]({case['source_url']})"
                )

        st.caption(
            "Current stage: rules and retrieval only. "
            "The LLM assessment has not been connected yet."
        )