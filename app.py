"""Streamlit entry point for the ClaimTrace screening interface."""

import streamlit as st

from src.rules_baseline import assess_by_rules
from src.ui_components import (
    inject_styles,
    render_boundary_notice,
    render_brand_header,
    render_case_card,
    render_empty_rule_details,
    render_risk_overview,
    render_rule_details,
    render_section_intro,
    render_sidebar,
    render_summary_card,
    render_workflow,
)
from src.ui_text import RISK_TEXT, t


st.set_page_config(
    page_title="ClaimTrace",
    page_icon="CT",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner=False)
def load_pipeline():
    """Load the retrieval model once and reuse it."""
    from src.risk_pipeline import ClaimTracePipeline

    return ClaimTracePipeline()


def initialise_state() -> None:
    """Create persistent UI state without overwriting existing input."""
    defaults = {
        "language": "zh",
        "language_selector": "中文",
        "claim_input": "",
        "assessment": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_language() -> None:
    """Keep the selected language in session state across reruns."""
    selected = st.session_state.get("language_selector", "中文")
    st.session_state["language"] = "zh" if selected == "中文" else "en"


def clear_assessment() -> None:
    """Remove a result that no longer matches the edited input."""
    st.session_state["assessment"] = None


def clear_claim() -> None:
    """Clear both the input and its previous result."""
    st.session_state["claim_input"] = ""
    clear_assessment()


def use_example(example_text: str) -> None:
    """Place one local example into the input without running the pipeline."""
    st.session_state["claim_input"] = example_text
    clear_assessment()


def yes_no(value: bool, lang: str) -> str:
    return t("yes", lang) if value else t("no", lang)


def risk_name(risk_level: str, lang: str) -> str:
    return RISK_TEXT.get(risk_level, RISK_TEXT["insufficient_evidence"])[lang][
        "name"
    ]


initialise_state()
inject_styles()

lang = st.session_state["language"]
render_sidebar(lang)

header_left, header_right = st.columns([4.8, 1.2], vertical_alignment="center")
with header_left:
    render_brand_header(lang)
with header_right:
    st.segmented_control(
        t("language_label", lang),
        options=["中文", "English"],
        key="language_selector",
        on_change=sync_language,
        label_visibility="collapsed",
        width="stretch",
    )

render_boundary_notice(lang)

input_column, workflow_column = st.columns([1.55, 1], gap="large")

with input_column:
    with st.container(border=True):
        render_section_intro(
            t("start_review", lang),
            t("start_review_help", lang),
            "01",
        )
        st.text_area(
            t("claim_label", lang),
            placeholder=t("claim_placeholder", lang),
            height=150,
            key="claim_input",
            on_change=clear_assessment,
        )
        st.caption(
            t(
                "character_count",
                lang,
                count=len(st.session_state["claim_input"]),
            )
        )

        st.markdown(f"**{t('try_example', lang)}**")
        example_columns = st.columns(3)
        examples = [
            ("example_high", "example_high_text"),
            ("example_evidence", "example_evidence_text"),
            ("example_low", "example_low_text"),
        ]
        for column, (label_key, text_key) in zip(example_columns, examples):
            with column:
                st.button(
                    t(label_key, lang),
                    key=f"use_{text_key}",
                    on_click=use_example,
                    args=(t(text_key, lang),),
                    use_container_width=True,
                )

        clear_column, assess_column = st.columns([1, 2.2])
        with clear_column:
            st.button(
                t("clear", lang),
                key="clear_claim_button",
                on_click=clear_claim,
                use_container_width=True,
            )
        with assess_column:
            assess_clicked = st.button(
                t("assess_claim", lang),
                type="primary",
                key="assess_claim_button",
                use_container_width=True,
            )

with workflow_column:
    with st.container(border=True):
        render_section_intro(
            t("workflow_title", lang),
            t("workflow_help", lang),
            "02",
        )
        render_workflow(lang)
        st.info(t("baseline_independent", lang), icon="ℹ️")

if assess_clicked:
    submitted_claim = st.session_state["claim_input"].strip()
    if not submitted_claim:
        st.warning(t("empty_input", lang), icon="⚠️")
    else:
        baseline_result = assess_by_rules(submitted_claim)
        try:
            with st.spinner(t("assessing", lang)):
                final_result = load_pipeline().assess(submitted_claim)
            st.session_state["assessment"] = {
                "claim": submitted_claim,
                "baseline": baseline_result,
                "final": final_result,
                "error_type": None,
            }
        except Exception as error:
            st.session_state["assessment"] = {
                "claim": submitted_claim,
                "baseline": baseline_result,
                "final": None,
                "error_type": type(error).__name__,
            }

assessment = st.session_state.get("assessment")

if assessment:
    st.divider()
    render_section_intro(
        t("results_title", lang),
        t("results_help", lang),
        "03",
    )

    baseline_result = assessment["baseline"]
    final_result = assessment["final"]
    error_type = assessment["error_type"]

    summary_columns = st.columns(4)
    render_summary_card(
        summary_columns[0],
        t("baseline_result", lang),
        risk_name(baseline_result["risk_level"], lang),
        t("independent_baseline", lang),
        baseline_result["risk_level"],
    )

    if final_result:
        retrieval = final_result["retrieval"]
        risk_card = final_result["risk_card"]
        top_score = f"{retrieval['top_score']:.4f}"
        final_risk = risk_card["risk_level"]
        needs_review = bool(risk_card["abstain"])
        review_detail = (
            t("review_required", lang)
            if needs_review
            else t("human_confirmation", lang)
        )
        render_summary_card(
            summary_columns[1],
            t("best_similarity", lang),
            top_score,
            t("text_similarity_only", lang),
            "similarity",
        )
        render_summary_card(
            summary_columns[2],
            t("final_risk", lang),
            risk_name(final_risk, lang),
            RISK_TEXT[final_risk][lang]["description"],
            final_risk,
        )
        render_summary_card(
            summary_columns[3],
            t("human_review", lang),
            yes_no(needs_review, lang),
            review_detail,
            "review" if needs_review else "confirmation",
        )
    else:
        retrieval = None
        risk_card = None
        render_summary_card(
            summary_columns[1],
            t("best_similarity", lang),
            t("not_available", lang),
            t("assessment_interrupted", lang),
            "similarity",
        )
        render_summary_card(
            summary_columns[2],
            t("final_risk", lang),
            t("assessment_incomplete", lang),
            t("no_automatic_conclusion", lang),
            "insufficient_evidence",
        )
        render_summary_card(
            summary_columns[3],
            t("human_review", lang),
            t("yes", lang),
            t("review_required", lang),
            "review",
        )

    tab_names = [
        t("tab_overview", lang),
        t("tab_cases", lang),
        t("tab_rules", lang),
        t("tab_technical", lang),
    ]
    overview_tab, cases_tab, rules_tab, technical_tab = st.tabs(tab_names)

    with overview_tab:
        if error_type:
            st.error(t("system_error", lang), icon="⚠️")
            st.write(t("system_error_action", lang))
        else:
            render_risk_overview(
                risk_card,
                final_result["llm_called"],
                lang,
            )

    with cases_tab:
        if retrieval and retrieval["retrieved_cases"]:
            st.caption(t("similarity_disclaimer", lang))
            for index, case in enumerate(retrieval["retrieved_cases"], start=1):
                render_case_card(case, index, lang)
        else:
            st.info(t("no_cases_available", lang))

    with rules_tab:
        if baseline_result["matched_terms"]:
            render_rule_details(assessment["claim"], lang)
        else:
            render_empty_rule_details(lang)
        st.caption(t("rule_scope_note", lang))

    with technical_tab:
        with st.expander(t("technical_expander", lang), expanded=False):
            if retrieval:
                technical_columns = st.columns(3)
                technical_columns[0].metric(
                    t("threshold", lang),
                    f"{retrieval['threshold']:.2f}",
                )
                technical_columns[1].metric(
                    t("llm_called", lang),
                    yes_no(final_result["llm_called"], lang),
                )
                technical_columns[2].metric(
                    t("model", lang),
                    final_result["model"] or t("not_called", lang),
                )
                st.caption(t("threshold_note", lang))

                usage = final_result.get("usage") or {}
                usage_fields = [
                    ("prompt_tokens", "prompt_tokens"),
                    ("completion_tokens", "completion_tokens"),
                    ("total_tokens", "request_total_tokens"),
                    ("cost", "request_cost"),
                ]
                reported_usage = [
                    (source_key, label_key)
                    for source_key, label_key in usage_fields
                    if usage.get(source_key) is not None
                ]
                if reported_usage:
                    st.markdown(f"**{t('single_request_usage', lang)}**")
                    usage_columns = st.columns(len(reported_usage))
                    for column, (source_key, label_key) in zip(
                        usage_columns, reported_usage
                    ):
                        value = usage[source_key]
                        if source_key == "cost":
                            value = f"${value}"
                        column.metric(t(label_key, lang), value)
                else:
                    st.caption(t("usage_not_reported", lang))
            else:
                st.write(f"**{t('model_error_type', lang)}:** `{error_type}`")
                st.caption(t("no_usage_on_error", lang))

    st.caption(t("final_responsibility", lang))
