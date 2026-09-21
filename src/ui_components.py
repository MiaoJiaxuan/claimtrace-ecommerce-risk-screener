"""Reusable presentation components for the ClaimTrace Streamlit UI."""

from html import escape

import streamlit as st

from src.rules_baseline import (
    EVIDENCE_PATTERNS,
    HIGH_RISK_PATTERNS,
    find_matches,
)
from src.ui_text import RISK_TEXT, t


def inject_styles() -> None:
    """Apply a small, class-scoped visual layer over the Streamlit theme."""
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1240px;
            padding-top: 4rem;
            padding-bottom: 3rem;
        }
        .ct-brand-kicker {
            color: #4f46e5;
            font-size: .76rem;
            font-weight: 750;
            letter-spacing: .12em;
            margin-bottom: .45rem;
        }
        .ct-brand-row {
            display: flex;
            align-items: baseline;
            flex-wrap: wrap;
            gap: .8rem;
        }
        .ct-brand-row h1 {
            color: #172033;
            font-size: clamp(2.25rem, 5vw, 3.8rem);
            letter-spacing: -.045em;
            line-height: 1;
            margin: 0;
        }
        .ct-brand-row span {
            color: #344054;
            font-size: 1.08rem;
            font-weight: 650;
        }
        .ct-brand-subtitle {
            color: #667085;
            font-size: .95rem;
            margin: .65rem 0 1.2rem;
        }
        .ct-notice {
            align-items: flex-start;
            background: #eef4ff;
            border: 1px solid #cddcff;
            border-radius: 14px;
            color: #243b66;
            display: flex;
            gap: .9rem;
            margin: .25rem 0 1.5rem;
            padding: 1rem 1.15rem;
        }
        .ct-notice-mark {
            align-items: center;
            background: #3157d5;
            border-radius: 999px;
            color: white;
            display: inline-flex;
            flex: 0 0 1.7rem;
            font-size: .85rem;
            font-weight: 800;
            height: 1.7rem;
            justify-content: center;
        }
        .ct-notice strong { display: block; margin-bottom: .15rem; }
        .ct-notice p { margin: 0; }
        .ct-section-head {
            align-items: flex-start;
            display: flex;
            gap: .85rem;
            margin-bottom: 1rem;
        }
        .ct-section-number {
            background: #edf0ff;
            border-radius: 8px;
            color: #4f46e5;
            font-size: .76rem;
            font-weight: 800;
            padding: .3rem .48rem;
        }
        .ct-section-head h2 {
            color: #172033;
            font-size: 1.22rem;
            margin: 0 0 .18rem;
        }
        .ct-section-head p { color: #667085; margin: 0; }
        .ct-workflow {
            display: grid;
            gap: .75rem;
            margin-bottom: 1rem;
        }
        .ct-workflow-step {
            border-left: 3px solid #aebbf5;
            padding: .1rem 0 .1rem .85rem;
        }
        .ct-workflow-step strong {
            color: #26324a;
            display: block;
            margin-bottom: .1rem;
        }
        .ct-workflow-step span { color: #667085; font-size: .88rem; }
        .ct-summary-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-top: 4px solid #64748b;
            border-radius: 12px;
            min-height: 148px;
            padding: 1rem;
        }
        .ct-summary-card.high_risk { border-top-color: #c9364f; }
        .ct-summary-card.evidence_needed { border-top-color: #d17b0f; }
        .ct-summary-card.low_risk { border-top-color: #16856b; }
        .ct-summary-card.insufficient_evidence,
        .ct-summary-card.review { border-top-color: #64748b; }
        .ct-summary-card.confirmation { border-top-color: #16856b; }
        .ct-summary-card.similarity { border-top-color: #3157d5; }
        .ct-summary-label {
            color: #667085;
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .02em;
            margin-bottom: .55rem;
            text-transform: uppercase;
        }
        .ct-summary-value {
            color: #172033;
            font-size: 1.12rem;
            font-weight: 750;
            line-height: 1.3;
            margin-bottom: .45rem;
        }
        .ct-summary-detail { color: #667085; font-size: .82rem; line-height: 1.4; }
        .ct-risk-banner {
            border: 1px solid #d9e0ea;
            border-left: 5px solid #64748b;
            border-radius: 12px;
            margin: .4rem 0 1rem;
            padding: 1rem 1.1rem;
        }
        .ct-risk-banner.high_risk { background: #fff3f4; border-left-color: #c9364f; }
        .ct-risk-banner.evidence_needed { background: #fff8eb; border-left-color: #d17b0f; }
        .ct-risk-banner.low_risk { background: #effaf6; border-left-color: #16856b; }
        .ct-risk-banner.insufficient_evidence { background: #f3f6f9; border-left-color: #64748b; }
        .ct-risk-title { color: #172033; font-size: 1.22rem; font-weight: 800; }
        .ct-risk-description { color: #475467; margin-top: .25rem; }
        .ct-sidebar-brand {
            color: #172033;
            font-size: 1.35rem;
            font-weight: 850;
            letter-spacing: -.025em;
            margin-bottom: .15rem;
        }
        .ct-sidebar-status { color: #667085; font-size: .83rem; margin-bottom: 1rem; }
        .ct-sidebar-rule { margin-bottom: .8rem; }
        .ct-sidebar-rule strong { color: #26324a; display: block; }
        .ct-sidebar-rule span { color: #667085; font-size: .86rem; line-height: 1.5; }
        @media (max-width: 800px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
            .ct-summary-card { min-height: auto; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header(lang: str) -> None:
    st.markdown(
        f"""
        <div class="ct-brand-kicker">{escape(t('page_eyebrow', lang))}</div>
        <div class="ct-brand-row">
            <h1>ClaimTrace</h1>
            <span>{escape(t('page_subtitle', lang))}</span>
        </div>
        <div class="ct-brand-subtitle">{escape(t('english_subtitle', lang))}</div>
        """,
        unsafe_allow_html=True,
    )


def render_boundary_notice(lang: str) -> None:
    st.markdown(
        f"""
        <div class="ct-notice">
            <span class="ct-notice-mark">i</span>
            <div>
                <strong>{escape(t('boundary_title', lang))}</strong>
                <p>{escape(t('boundary_text', lang))}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(title: str, help_text: str, number: str) -> None:
    st.markdown(
        f"""
        <div class="ct-section-head">
            <span class="ct-section-number">{escape(number)}</span>
            <div><h2>{escape(title)}</h2><p>{escape(help_text)}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow(lang: str) -> None:
    steps = [
        ("workflow_rule", "workflow_rule_help"),
        ("workflow_retrieval", "workflow_retrieval_help"),
        ("workflow_threshold", "workflow_threshold_help"),
        ("workflow_decision", "workflow_decision_help"),
    ]
    content = "".join(
        (
            '<div class="ct-workflow-step">'
            f"<strong>{index}. {escape(t(title_key, lang))}</strong>"
            f"<span>{escape(t(help_key, lang))}</span>"
            "</div>"
        )
        for index, (title_key, help_key) in enumerate(steps, start=1)
    )
    st.markdown(
        f'<div class="ct-workflow">{content}</div>',
        unsafe_allow_html=True,
    )


def render_summary_card(
    column: object,
    label: str,
    value: str,
    detail: str,
    tone: str,
) -> None:
    with column:
        st.markdown(
            f"""
            <div class="ct-summary-card {escape(tone)}">
                <div class="ct-summary-label">{escape(label)}</div>
                <div class="ct-summary-value">{escape(str(value))}</div>
                <div class="ct-summary-detail">{escape(detail)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_risk_overview(risk_card: dict, llm_called: bool, lang: str) -> None:
    risk_level = risk_card["risk_level"]
    risk_copy = RISK_TEXT.get(
        risk_level,
        RISK_TEXT["insufficient_evidence"],
    )[lang]
    st.markdown(
        f"""
        <div class="ct-risk-banner {escape(risk_level)}">
            <div class="ct-risk-title">
                {escape(risk_copy['icon'])} {escape(risk_copy['name'])}
            </div>
            <div class="ct-risk-description">{escape(risk_copy['description'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown(f"**{t('highlighted_claim', lang)}**")
        st.info(risk_card.get("highlighted_claim") or t("none", lang))

        reason_label = (
            t("model_original_reason", lang)
            if llm_called
            else t("system_explanation", lang)
        )
        reason = risk_card.get("reason") or t("none", lang)
        if not llm_called and risk_level == "insufficient_evidence":
            reason = t("retrieval_below_threshold", lang)
        st.markdown(f"**{reason_label}**")
        st.write(reason)

        action_label = (
            t("model_original_action", lang)
            if llm_called
            else t("next_action", lang)
        )
        action = risk_card.get("next_action") or risk_copy["action"]
        if not llm_called and risk_level == "insufficient_evidence":
            action = t("send_human_review", lang)
        st.markdown(f"**{action_label}**")
        st.write(action)

    with right:
        st.markdown(f"**{t('risk_level', lang)}**")
        st.write(risk_copy["name"])
        st.markdown(f"**{t('abstained', lang)}**")
        st.write(t("yes", lang) if risk_card.get("abstain") else t("no", lang))
        st.markdown(f"**{t('confidence', lang)}**")
        if llm_called:
            st.write(f"{risk_card.get('confidence', 0.0):.2f}")
            st.caption(t("confidence_note", lang))
        else:
            st.write(t("not_available", lang))

        if risk_card.get("source_title"):
            st.markdown(f"**{t('supporting_source', lang)}**")
            st.write(risk_card["source_title"])
        if risk_card.get("source_url"):
            st.link_button(
                t("open_cited_source", lang),
                risk_card["source_url"],
                use_container_width=True,
            )

    st.info(t("fixed_human_notice", lang), icon="ℹ️")


def render_case_card(case: dict, index: int, lang: str) -> None:
    with st.container(border=True):
        title_column, score_column = st.columns([4, 1])
        with title_column:
            st.markdown(
                f"**{t('case_rank', lang, index=index)} · "
                f"{escape(str(case['title']))}**"
            )
            st.caption(f"{t('case_id', lang)}: {case['case_id']}")
        with score_column:
            st.metric(
                t("text_similarity", lang),
                f"{case['similarity_score']:.4f}",
            )

        st.write(f"**{t('risk_type', lang)}:** `{case['risk_type']}`")
        with st.expander(t("case_summary", lang)):
            st.write(case["case_text"])
        st.link_button(
            t("official_source", lang),
            case["source_url"],
            use_container_width=False,
        )


def _rule_key(pattern: str) -> str:
    if "彻底治愈" in pattern:
        return "rule_medical"
    if "国家级" in pattern:
        return "rule_superlative"
    if "销量" in pattern:
        return "rule_sales"
    if "元" in pattern:
        return "rule_price"
    return "rule_effect"


def render_rule_details(claim: str, lang: str) -> None:
    rule_groups = [
        ("high_risk", HIGH_RISK_PATTERNS),
        ("evidence_needed", EVIDENCE_PATTERNS),
    ]
    displayed = set()
    for risk_level, patterns in rule_groups:
        for pattern, _ in patterns:
            for match in find_matches(claim, [(pattern, "")]):
                item = (match["text"], pattern)
                if item in displayed:
                    continue
                displayed.add(item)
                with st.container(border=True):
                    fragment_column, explanation_column = st.columns([1, 2])
                    fragment_column.markdown(
                        f"**{t('matched_fragment', lang)}**\n\n"
                        f"`{match['text']}`"
                    )
                    explanation_column.markdown(
                        f"**{t('rule_explanation', lang)}**\n\n"
                        f"{t(_rule_key(pattern), lang)}"
                    )
                    st.caption(RISK_TEXT[risk_level][lang]["name"])


def render_empty_rule_details(lang: str) -> None:
    st.info(t("no_rule_match", lang))
    st.write(t("no_rule_match_help", lang))


def render_sidebar(lang: str) -> None:
    with st.sidebar:
        st.markdown(
            '<div class="ct-sidebar-brand">ClaimTrace</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ct-sidebar-status">{escape(t("sidebar_status", lang))}</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown(f"### {t('sidebar_guide', lang)}")
        rule_items = [
            ("rule_high_title", "rule_high_body"),
            ("rule_evidence_title", "rule_evidence_body"),
            ("rule_low_title", "rule_low_body"),
            ("rule_insufficient_title", "rule_insufficient_body"),
        ]
        for title_key, body_key in rule_items:
            st.markdown(
                f"""
                <div class="ct-sidebar-rule">
                    <strong>{escape(t(title_key, lang))}</strong>
                    <span>{escape(t(body_key, lang))}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander(t("sidebar_limits", lang), expanded=False):
            for key in [
                "limit_rules",
                "limit_cases",
                "limit_citation",
                "limit_threshold",
                "limit_human",
            ]:
                st.markdown(f"- {t(key, lang)}")
