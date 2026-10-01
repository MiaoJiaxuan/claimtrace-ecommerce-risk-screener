"""Streamlit entry point for the ClaimTrace screening interface."""

from pathlib import Path

import streamlit as st

from src.rules_baseline import assess_by_rules
from src.ui_components import (
    inject_styles,
    render_boundary_notice,
    render_brand_header,
    render_case_card,
    render_decision_hero,
    render_empty_trail,
    render_empty_rule_details,
    render_hero_visual,
    render_intro_marker,
    render_reference_rules,
    render_reason_action,
    render_rule_details,
    render_section_intro,
    render_top_bar,
    render_trace_path,
    render_workbench_result,
    render_workflow,
)
from src.ui_text import t


ROOT = Path(__file__).resolve().parent
HERO_IMAGE = ROOT / "assets" / "claimtrace-evidence-flow.png"


st.set_page_config(
    page_title="ClaimTrace",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        "intro_played": False,
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


initialise_state()
inject_styles()

lang = st.session_state["language"]
intro_active = not st.session_state["intro_played"]
render_intro_marker(intro_active)

top_brand, top_language = st.columns([4.5, 1.5], vertical_alignment="center")
with top_brand:
    render_top_bar(lang, intro_active)
with top_language:
    st.segmented_control(
        t("language_label", lang),
        options=["中文", "English"],
        key="language_selector",
        on_change=sync_language,
        label_visibility="collapsed",
        width="stretch",
    )

hero_copy, hero_visual = st.columns([1.15, 1], gap="large", vertical_alignment="center")
with hero_copy:
    render_brand_header(lang, intro_active)
with hero_visual:
    render_hero_visual(HERO_IMAGE, lang, intro_active)

render_boundary_notice(lang, intro_active)

with st.container(key="claimtrace_workbench"):
    input_column, result_column = st.columns([1.45, 1], gap="large")

    with input_column:
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

    with result_column:
        render_section_intro(
            t("results_title", lang),
            t("results_help", lang),
            "02",
        )
        workbench_assessment = st.session_state.get("assessment")
        if workbench_assessment:
            preview_final = workbench_assessment["final"]
            preview_retrieval = preview_final["retrieval"] if preview_final else None
            preview_card = (
                preview_final["risk_card"]
                if preview_final
                else {
                    "risk_level": "insufficient_evidence",
                    "abstain": True,
                }
            )
            render_workbench_result(preview_card, preview_retrieval, lang)
        else:
            render_empty_trail(lang)

with st.container(key="claimtrace_workflow"):
    render_section_intro(
        t("workflow_title", lang),
        t("workflow_help", lang),
        "03",
    )
    render_workflow(lang)

with st.container(key="claimtrace_rules"):
    render_section_intro(
        t("reference_rules_title", lang),
        t("reference_rules_help", lang),
        "04",
    )
    render_reference_rules(lang)

st.session_state["intro_played"] = True

assessment = st.session_state.get("assessment")

if assessment:
    st.divider()
    render_section_intro(
        t("results_title", lang),
        t("results_help", lang),
        "05",
    )

    baseline_result = assessment["baseline"]
    final_result = assessment["final"]
    error_type = assessment["error_type"]

    if final_result:
        retrieval = final_result["retrieval"]
        risk_card = final_result["risk_card"]
        llm_called = bool(final_result["llm_called"])
    else:
        retrieval = None
        llm_called = False
        risk_card = {
            "risk_level": "insufficient_evidence",
            "abstain": True,
            # A failed assessment has no verified exact-span highlight.
            "highlighted_claim": "",
            "reason": t("assessment_interrupted", lang),
            "next_action": t("system_error_action", lang),
            "source_title": None,
            "source_url": None,
        }

    if error_type:
        st.error(t("system_error", lang), icon="⚠️")

    render_decision_hero(
        risk_card,
        llm_called,
        baseline_result,
        retrieval,
        lang,
        bool(error_type),
    )
    render_trace_path(
        baseline_result,
        retrieval,
        llm_called,
        bool(error_type),
        lang,
    )

    evidence_tab, technical_tab = st.tabs(
        [t("tab_evidence", lang), t("tab_technical", lang)]
    )

    with evidence_tab:
        render_reason_action(risk_card, llm_called, lang, bool(error_type))
        st.caption(t("language_content_note", lang))

        highlighted_claim = risk_card.get("highlighted_claim")
        if highlighted_claim:
            st.markdown(f"### {t('highlighted_claim', lang)}")
            st.info(highlighted_claim)

        if risk_card.get("source_title"):
            st.markdown(f"### {t('supporting_source', lang)}")
            st.write(risk_card["source_title"])
            if risk_card.get("source_url"):
                st.link_button(
                    t("open_cited_source", lang),
                    risk_card["source_url"],
                )

        st.markdown(f"### {t('rule_findings', lang)}")
        if baseline_result["matched_terms"]:
            render_rule_details(assessment["claim"], lang)
        else:
            render_empty_rule_details(lang)
        st.caption(t("rule_scope_note", lang))

        st.markdown(f"### {t('case_sources', lang)}")
        st.caption(t("similarity_disclaimer", lang))
        if retrieval and retrieval["retrieved_cases"]:
            case_columns = st.columns(3, gap="medium")
            for index, (column, case) in enumerate(
                zip(case_columns, retrieval["retrieved_cases"]),
                start=1,
            ):
                with column:
                    render_case_card(case, index, lang)
        else:
            st.info(t("no_cases_available", lang))

    with technical_tab:
        if retrieval and final_result:
            technical_columns = st.columns(3)
            technical_columns[0].metric(
                t("threshold", lang),
                f"{retrieval['threshold']:.2f}",
            )
            technical_columns[1].metric(
                t("llm_called", lang),
                t("yes", lang) if final_result["llm_called"] else t("no", lang),
            )
            technical_columns[2].metric(
                t("model", lang),
                final_result["model"] or t("not_called", lang),
            )
            st.caption(t("threshold_note", lang))

            if final_result["llm_called"]:
                st.markdown(f"**{t('confidence', lang)}**")
                st.write(f"{risk_card.get('confidence', 0.0):.2f}")
                st.caption(t("confidence_note", lang))

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
                    usage_columns,
                    reported_usage,
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

        st.info(t("technical_boundary", lang), icon="ℹ️")

    st.caption(t("final_responsibility", lang))
