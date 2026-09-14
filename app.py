import streamlit as st

from src.risk_pipeline import ClaimTracePipeline
from src.rules_baseline import assess_by_rules


st.set_page_config(
    page_title="ClaimTrace",
    page_icon="🔎",
    layout="centered",
)


@st.cache_resource(show_spinner="Loading the retrieval model...")
def load_pipeline() -> ClaimTracePipeline:
    """Load the retrieval model once and reuse it."""
    return ClaimTracePipeline()


def show_risk_level(risk_level: str) -> None:
    """Display one risk level using a suitable Streamlit message."""
    if risk_level == "high_risk":
        st.error("High risk")
    elif risk_level == "evidence_needed":
        st.warning("Evidence needed")
    elif risk_level == "low_risk":
        st.success("No configured concern identified")
    else:
        st.info("Insufficient evidence")


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
        st.stop()

    baseline_result = assess_by_rules(claim)

    st.subheader("1. Rule-based baseline")
    show_risk_level(baseline_result["risk_level"])

    st.write("**Matched text:**")

    if baseline_result["matched_terms"]:
        st.write(", ".join(baseline_result["matched_terms"]))
    else:
        st.write("None")

    st.write("**Reason:**")
    st.write(baseline_result["reason"])

    try:
        with st.spinner(
            "Retrieving evidence and preparing the assessment..."
        ):
            pipeline = load_pipeline()
            final_result = pipeline.assess(claim)
    except Exception as error:
        st.divider()
        st.subheader("System status")
        st.error(
            "The assessment could not be completed. "
            "Human review is required."
        )
        st.caption(f"Error type: {type(error).__name__}")
        st.stop()

    retrieval_result = final_result["retrieval"]

    st.divider()
    st.subheader("2. Retrieved evidence")

    if retrieval_result["abstain"]:
        st.warning("Insufficient evidence — human review required.")
    else:
        st.success("Relevant evidence found.")

    st.write(
        f"Top similarity score: "
        f"{retrieval_result['top_score']:.4f}"
    )

    st.caption(
        f"Provisional threshold: "
        f"{retrieval_result['threshold']:.2f}. "
        "This threshold will be calibrated using the development set."
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

    st.divider()
    st.subheader("3. Structured risk card")

    risk_card = final_result["risk_card"]
    show_risk_level(risk_card["risk_level"])

    if not final_result["llm_called"]:
        st.warning(
            "The LLM was not called because the retrieved evidence "
            "was below the threshold."
        )

    st.write("**Highlighted claim:**")
    st.write(risk_card["highlighted_claim"] or "None")

    st.write("**Reason:**")
    st.write(risk_card["reason"])

    st.write("**Next action:**")
    st.write(risk_card["next_action"])

    st.write("**Confidence:**")
    st.write(f"{risk_card['confidence']:.2f}")

    st.write("**Abstained:**")
    st.write("Yes" if risk_card["abstain"] else "No")

    if risk_card["source_title"]:
        st.write("**Supporting source:**")
        st.write(risk_card["source_title"])

    if risk_card["source_url"]:
        st.markdown(
            f"[Open the cited official source]"
            f"({risk_card['source_url']})"
        )

    if final_result["llm_called"]:
        usage = final_result["usage"]

        st.divider()
        st.subheader("4. Model usage")

        st.write(f"Model: `{final_result['model']}`")
        st.write(
            f"Prompt tokens: "
            f"{usage.get('prompt_tokens', 'Not reported')}"
        )
        st.write(
            f"Completion tokens: "
            f"{usage.get('completion_tokens', 'Not reported')}"
        )
        st.write(
            f"Total tokens: "
            f"{usage.get('total_tokens', 'Not reported')}"
        )
        st.write(
            f"Reported cost: "
            f"${usage.get('cost', 'Not reported')}"
        )

    st.caption(
        "A human remains responsible for the final publication decision."
    )