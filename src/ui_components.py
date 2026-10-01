"""Reusable presentation components for the ClaimTrace Streamlit UI."""

import base64
from functools import lru_cache
from html import escape
from pathlib import Path

import streamlit as st

from src.rules_baseline import (
    EVIDENCE_PATTERNS,
    HIGH_RISK_PATTERNS,
    find_matches,
)
from src.ui_text import RISK_TEXT, t


STYLE_PATH = Path(__file__).resolve().parents[1] / "tokens.css"


def inject_styles() -> None:
    """Apply the ClaimTrace token-driven visual system."""
    if STYLE_PATH.exists():
        st.markdown(
            f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )
        return
    st.markdown(
        """
        <style>
        :root {
            --ct-ink: #172033;
            --ct-muted: #667085;
            --ct-line: #dfe5ef;
            --ct-indigo: #3157d5;
            --ct-teal: #16856b;
            --ct-amber: #d17b0f;
            --ct-coral: #c9364f;
            --ct-slate: #64748b;
        }
        .stApp {
            background:
                radial-gradient(circle at 86% 4%, rgba(49,87,213,.08), transparent 25rem),
                linear-gradient(180deg, #f8faff 0, #f5f7fb 22rem, #f5f7fb 100%);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2.25rem;
            padding-bottom: 3.5rem;
        }
        header[data-testid="stHeader"] { background: transparent; }
        [data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; }

        .ct-brand-kicker {
            color: var(--ct-indigo);
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .13em;
            margin-bottom: .65rem;
        }
        .ct-brand-row {
            align-items: center;
            display: flex;
            gap: .8rem;
        }
        .ct-brand-mark {
            align-items: center;
            background: linear-gradient(145deg, #3157d5, #243f9c);
            border-radius: 14px;
            box-shadow: 0 10px 24px rgba(49,87,213,.20);
            color: white;
            display: inline-flex;
            font-size: .86rem;
            font-weight: 850;
            height: 2.65rem;
            justify-content: center;
            letter-spacing: -.03em;
            width: 2.65rem;
        }
        .ct-brand-row h1 {
            color: var(--ct-ink);
            font-size: clamp(2.5rem, 5vw, 4.25rem);
            letter-spacing: -.055em;
            line-height: .95;
            margin: 0;
        }
        .ct-brand-subtitle {
            color: #344054;
            font-size: clamp(1rem, 2vw, 1.28rem);
            font-weight: 650;
            margin: 1.15rem 0 .45rem;
        }
        .ct-brand-promise {
            color: var(--ct-muted);
            font-size: .98rem;
            line-height: 1.65;
            margin-bottom: 1rem;
            max-width: 40rem;
        }
        .ct-trust-row { display: flex; flex-wrap: wrap; gap: .5rem; }
        .ct-trust-pill {
            background: rgba(255,255,255,.75);
            border: 1px solid #d9e1f2;
            border-radius: 999px;
            color: #40516e;
            font-size: .78rem;
            font-weight: 650;
            padding: .36rem .68rem;
        }
        .ct-hero-visual {
            align-items: center;
            display: flex;
            justify-content: center;
            min-height: 250px;
            padding: .25rem 0 .5rem;
        }

        .ct-notice {
            align-items: center;
            background: rgba(238,244,255,.84);
            border: 1px solid #cddcff;
            border-radius: 12px;
            color: #243b66;
            display: flex;
            gap: .75rem;
            margin: .35rem 0 1.35rem;
            padding: .75rem .9rem;
        }
        .ct-notice-mark {
            align-items: center;
            background: var(--ct-indigo);
            border-radius: 999px;
            color: white;
            display: inline-flex;
            flex: 0 0 1.55rem;
            font-size: .76rem;
            font-weight: 800;
            height: 1.55rem;
            justify-content: center;
        }
        .ct-notice strong { margin-right: .35rem; }
        .ct-notice p { display: inline; margin: 0; }

        .ct-section-head {
            align-items: flex-start;
            display: flex;
            gap: .8rem;
            margin-bottom: 1rem;
        }
        .ct-section-number {
            background: #edf0ff;
            border-radius: 8px;
            color: #4f46e5;
            font-size: .74rem;
            font-weight: 800;
            padding: .32rem .5rem;
        }
        .ct-section-head h2 {
            color: var(--ct-ink);
            font-size: 1.24rem;
            margin: 0 0 .18rem;
        }
        .ct-section-head p { color: var(--ct-muted); margin: 0; }

        .ct-workbench {
            background: rgba(255,255,255,.88);
            border: 1px solid var(--ct-line);
            border-radius: 18px;
            box-shadow: 0 12px 34px rgba(23,32,51,.055);
            margin-bottom: 1rem;
            padding: 1.2rem;
        }
        .ct-workflow {
            background: #f8faff;
            border: 1px solid #e0e7f6;
            border-radius: 14px;
            display: grid;
            gap: .75rem;
            margin-bottom: .75rem;
            padding: .95rem;
        }
        .ct-workflow-step { display: grid; gap: .12rem; grid-template-columns: 1.65rem 1fr; }
        .ct-workflow-index {
            align-items: center;
            background: #e8edff;
            border-radius: 999px;
            color: var(--ct-indigo);
            display: inline-flex;
            font-size: .7rem;
            font-weight: 800;
            height: 1.45rem;
            justify-content: center;
            width: 1.45rem;
        }
        .ct-workflow-step strong { color: #26324a; display: block; font-size: .9rem; }
        .ct-workflow-step span { color: var(--ct-muted); font-size: .81rem; line-height: 1.45; }
        .ct-baseline-note {
            background: #fff;
            border: 1px dashed #cbd5e1;
            border-radius: 10px;
            color: #475467;
            font-size: .82rem;
            line-height: 1.5;
            padding: .65rem .75rem;
        }
        .ct-principles { display: grid; gap: .48rem; margin-top: .8rem; }
        .ct-principle {
            align-items: flex-start;
            display: grid;
            gap: .55rem;
            grid-template-columns: .55rem 1fr;
        }
        .ct-principle-dot {
            background: var(--ct-teal);
            border-radius: 999px;
            height: .42rem;
            margin-top: .42rem;
            width: .42rem;
        }
        .ct-principle strong { color: #344054; display: block; font-size: .84rem; }
        .ct-principle span { color: var(--ct-muted); font-size: .79rem; line-height: 1.42; }

        .ct-decision {
            background: #fff;
            border: 1px solid var(--ct-line);
            border-left: 7px solid var(--ct-slate);
            border-radius: 18px;
            box-shadow: 0 15px 38px rgba(23,32,51,.065);
            margin: .35rem 0 1rem;
            overflow: hidden;
            padding: 1.3rem 1.4rem 1.15rem;
        }
        .ct-decision.high_risk { background: linear-gradient(110deg, #fff5f6, #fff); border-left-color: var(--ct-coral); }
        .ct-decision.evidence_needed { background: linear-gradient(110deg, #fff9ee, #fff); border-left-color: var(--ct-amber); }
        .ct-decision.low_risk { background: linear-gradient(110deg, #f0fbf7, #fff); border-left-color: var(--ct-teal); }
        .ct-decision.insufficient_evidence { background: linear-gradient(110deg, #f3f6f9, #fff); border-left-color: var(--ct-slate); }
        .ct-decision-top { align-items: center; display: flex; gap: .9rem; }
        .ct-status-icon {
            align-items: center;
            background: #eef2f7;
            border-radius: 13px;
            color: var(--ct-slate);
            display: inline-flex;
            flex: 0 0 2.6rem;
            font-size: 1.25rem;
            font-weight: 850;
            height: 2.6rem;
            justify-content: center;
        }
        .high_risk .ct-status-icon { background: #ffe3e7; color: var(--ct-coral); }
        .evidence_needed .ct-status-icon { background: #fff0ce; color: var(--ct-amber); }
        .low_risk .ct-status-icon { background: #dff5ec; color: var(--ct-teal); }
        .ct-decision-label { color: var(--ct-muted); font-size: .73rem; font-weight: 750; letter-spacing: .08em; text-transform: uppercase; }
        .ct-decision h2 { color: var(--ct-ink); font-size: clamp(1.55rem, 3vw, 2.05rem); margin: .08rem 0 .18rem; }
        .ct-decision-description { color: #475467; font-size: .94rem; }
        .ct-decision-action {
            background: rgba(255,255,255,.75);
            border: 1px solid rgba(203,213,225,.8);
            border-radius: 11px;
            color: #344054;
            margin-top: 1rem;
            padding: .75rem .9rem;
        }
        .ct-decision-action strong { color: var(--ct-ink); }
        .ct-decision-meta { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .9rem; }
        .ct-meta-pill {
            background: #fff;
            border: 1px solid #dbe3ee;
            border-radius: 999px;
            color: #475467;
            font-size: .76rem;
            padding: .34rem .62rem;
        }

        .ct-trace-wrap {
            background: #fff;
            border: 1px solid var(--ct-line);
            border-radius: 16px;
            margin: 0 0 1.15rem;
            padding: 1rem 1.05rem;
        }
        .ct-trace-title { color: var(--ct-ink); font-size: .98rem; font-weight: 800; }
        .ct-trace-subtitle { color: var(--ct-muted); font-size: .8rem; margin: .12rem 0 .75rem; }
        .ct-trace-baseline {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 9px;
            color: #475467;
            font-size: .79rem;
            margin-bottom: .7rem;
            padding: .55rem .7rem;
        }
        .ct-trace-grid { display: grid; gap: .65rem; grid-template-columns: repeat(3, minmax(0, 1fr)); }
        .ct-trace-step {
            background: #f8faff;
            border: 1px solid #e1e7f4;
            border-radius: 11px;
            min-height: 94px;
            padding: .72rem .78rem;
            position: relative;
        }
        .ct-trace-step:not(:last-child)::after {
            color: #93a4c8;
            content: '→';
            font-size: 1rem;
            position: absolute;
            right: -.56rem;
            top: 2.15rem;
            z-index: 2;
        }
        .ct-trace-step small { color: var(--ct-indigo); font-size: .66rem; font-weight: 800; letter-spacing: .06em; }
        .ct-trace-step strong { color: #26324a; display: block; font-size: .86rem; margin: .23rem 0 .12rem; }
        .ct-trace-step span { color: var(--ct-muted); font-size: .76rem; line-height: 1.42; }

        .ct-direct-card {
            background: #fff;
            border: 1px solid var(--ct-line);
            border-radius: 14px;
            min-height: 150px;
            padding: 1rem;
        }
        .ct-direct-card-label { color: var(--ct-indigo); font-size: .72rem; font-weight: 800; letter-spacing: .08em; margin-bottom: .48rem; text-transform: uppercase; }
        .ct-direct-card h3 { color: var(--ct-ink); font-size: 1rem; margin: 0 0 .45rem; }
        .ct-direct-card p { color: #475467; font-size: .88rem; line-height: 1.62; margin: 0; }

        .ct-case-card {
            background: #fff;
            border: 1px solid var(--ct-line);
            border-radius: 14px;
            min-height: 220px;
            padding: .95rem;
        }
        .ct-case-rank { color: var(--ct-indigo); font-size: .7rem; font-weight: 800; letter-spacing: .08em; }
        .ct-case-card h4 { color: var(--ct-ink); font-size: .92rem; line-height: 1.45; margin: .35rem 0 .5rem; }
        .ct-case-score { color: #344054; font-size: .8rem; font-weight: 700; margin-bottom: .55rem; }
        .ct-case-card p {
            color: var(--ct-muted);
            display: -webkit-box;
            font-size: .79rem;
            line-height: 1.5;
            margin: 0 0 .5rem;
            overflow: hidden;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 4;
        }
        .ct-case-tag { background: #f0f4fb; border-radius: 999px; color: #475467; display: inline-block; font-size: .7rem; padding: .24rem .46rem; }

        .ct-sidebar-brand { color: var(--ct-ink); font-size: 1.28rem; font-weight: 850; letter-spacing: -.025em; }
        .ct-sidebar-status { color: var(--ct-muted); font-size: .8rem; margin: .12rem 0 .9rem; }
        .ct-sidebar-legend { display: grid; gap: .48rem; }
        .ct-legend-row {
            align-items: center;
            background: rgba(255,255,255,.72);
            border: 1px solid #dce3ed;
            border-radius: 9px;
            display: grid;
            gap: .5rem;
            grid-template-columns: 1.55rem 1fr;
            padding: .5rem .6rem;
        }
        .ct-legend-icon {
            align-items: center;
            background: #edf1f6;
            border-radius: 7px;
            color: var(--ct-slate);
            display: inline-flex;
            font-size: .72rem;
            font-weight: 850;
            height: 1.45rem;
            justify-content: center;
            width: 1.45rem;
        }
        .ct-legend-row.high_risk .ct-legend-icon { background: #ffe3e7; color: var(--ct-coral); }
        .ct-legend-row.evidence_needed .ct-legend-icon { background: #fff0ce; color: var(--ct-amber); }
        .ct-legend-row.low_risk .ct-legend-icon { background: #dff5ec; color: var(--ct-teal); }
        .ct-legend-row strong { color: #344054; font-size: .8rem; }
        .ct-sidebar-boundary { color: #5a687f; font-size: .79rem; line-height: 1.55; }

        div[data-testid="stButton"] button[kind="primary"] {
            box-shadow: 0 8px 18px rgba(49,87,213,.18);
            font-weight: 750;
        }
        div[data-testid="stTabs"] button { font-weight: 700; }

        @media (max-width: 800px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1.25rem; }
            .ct-hero-visual { min-height: auto; }
            .ct-brand-row h1 { font-size: 2.65rem; }
            .ct-notice { align-items: flex-start; }
            .ct-notice strong, .ct-notice p { display: block; }
            .ct-trace-grid { grid-template-columns: 1fr; }
            .ct-trace-step:not(:last-child)::after { bottom: -.75rem; content: '↓'; left: 50%; right: auto; top: auto; }
            .ct-case-card, .ct-direct-card { min-height: auto; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if STYLE_PATH.exists():
        st.markdown(
            f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def _intro_class(animate: bool) -> str:
    return " ct-intro-on" if animate else ""


@lru_cache(maxsize=4)
def _image_data_uri(path_value: str) -> str:
    """Return a local PNG as a data URI without Streamlit image processing."""
    image_path = Path(path_value)
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_intro_marker(active: bool) -> None:
    if active:
        st.markdown(
            '<span class="ct-intro-marker" aria-hidden="true"></span>',
            unsafe_allow_html=True,
        )


def render_top_bar(lang: str, animate: bool = False) -> None:
    st.markdown(
        f"""
        <div class="ct-topbar{_intro_class(animate)}">
            <span class="ct-wordmark">ClaimTrace</span>
            <span class="ct-status-badge">{escape(t('preliminary_status', lang))}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header(lang: str, animate: bool = False) -> None:
    st.markdown(
        f"""
        <div class="ct-hero-copy{_intro_class(animate)}">
            <div class="ct-brand-kicker">{escape(t('page_eyebrow', lang))}</div>
            <h1>{escape(t('page_headline', lang))}</h1>
            <div class="ct-brand-subtitle">{escape(t('page_subtitle', lang))}</div>
            <p class="ct-brand-promise">{escape(t('brand_promise', lang))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_visual(
    image_path: Path,
    lang: str,
    animate: bool = False,
) -> None:
    data_uri = _image_data_uri(str(image_path.resolve()))
    image_html = (
        f'<img src="{data_uri}" alt="{escape(t("hero_visual_alt", lang))}">'
        if data_uri
        else ""
    )
    nodes = [
        t("visual_input", lang),
        t("visual_evidence", lang),
        t("visual_review", lang),
    ]
    nodes_html = "".join(
        f'<div class="ct-visual-node"><b></b><span>{escape(item)}</span></div>'
        for item in nodes
    )
    st.markdown(
        f"""
        <figure class="ct-hero-visual{_intro_class(animate)}">
            <div class="ct-visual-header">
                <span>{escape(t('visual_title', lang))}</span>
            </div>
            {image_html}
            <figcaption class="ct-visual-trail">{nodes_html}</figcaption>
        </figure>
        """,
        unsafe_allow_html=True,
    )


def render_boundary_notice(lang: str, animate: bool = False) -> None:
    st.markdown(
        f"""
        <div class="ct-notice{_intro_class(animate)}">
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
        ("workflow_input", "workflow_input_help"),
        ("workflow_retrieval", "workflow_retrieval_help"),
        ("workflow_decision", "workflow_decision_help"),
    ]
    content = "".join(
        (
            '<div class="ct-workflow-step">'
            f'<span class="ct-workflow-index">{index}</span>'
            "<div>"
            f"<strong>{escape(t(title_key, lang))}</strong>"
            f"<span>{escape(t(help_key, lang))}</span>"
            "</div></div>"
        )
        for index, (title_key, help_key) in enumerate(steps, start=1)
    )
    st.markdown(
        f"""
        <div class="ct-workflow-shell">
            <div class="ct-workflow">{content}</div>
            <div class="ct-baseline-note">
                <strong>{escape(t('workflow_rule', lang))}：</strong>
                {escape(t('baseline_independent', lang))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_trail(lang: str) -> None:
    steps = [
        ("visual_input", "empty_input_step"),
        ("visual_evidence", "empty_evidence_step"),
        ("visual_review", "empty_review_step"),
    ]
    steps_html = "".join(
        (
            '<div class="ct-empty-step"><b aria-hidden="true"></b><div>'
            f'<strong>{escape(t(title_key, lang))}</strong>'
            f'<span>{escape(t(body_key, lang))}</span>'
            "</div></div>"
        )
        for title_key, body_key in steps
    )
    st.markdown(
        f"""
        <div class="ct-empty-trail">
            <div class="ct-empty-label">{escape(t('empty_state_label', lang))}</div>
            <h3>{escape(t('empty_state_title', lang))}</h3>
            <div class="ct-empty-steps">{steps_html}</div>
            <p class="ct-empty-note">{escape(t('empty_state_note', lang))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workbench_result(
    risk_card: dict,
    retrieval: dict | None,
    lang: str,
) -> None:
    risk_level = risk_card.get("risk_level", "insufficient_evidence")
    risk_copy = RISK_TEXT.get(
        risk_level,
        RISK_TEXT["insufficient_evidence"],
    )[lang]
    score = (
        f"{retrieval['top_score']:.4f}"
        if retrieval and retrieval.get("top_score") is not None
        else t("not_available", lang)
    )
    routed = t("yes", lang) if risk_card.get("abstain") else t("no", lang)
    st.markdown(
        f"""
        <div class="ct-ready-result {escape(risk_level)}">
            <div class="ct-empty-label">{escape(t('result_ready', lang))}</div>
            <h3>{escape(risk_copy['name'])}</h3>
            <p>{escape(risk_copy['description'])}</p>
            <div class="ct-ready-facts">
                <div class="ct-ready-fact">
                    <small>{escape(t('best_similarity', lang))}</small>
                    <strong>{escape(score)}</strong>
                </div>
                <div class="ct-ready-fact">
                    <small>{escape(t('human_review', lang))}</small>
                    <strong>{escape(routed)}</strong>
                </div>
            </div>
            <p class="ct-empty-note">{escape(t('result_ready_help', lang))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_reference_rules(lang: str) -> None:
    items = [
        ("high_risk", "rule_high_title", "rule_high_body"),
        ("evidence_needed", "rule_evidence_title", "rule_evidence_body"),
        ("low_risk", "rule_low_title", "rule_low_body"),
    ]
    cards = "".join(
        (
            f'<article class="ct-rule-reference {risk_level}">'
            f'<div class="ct-rule-code"><i aria-hidden="true"></i>{risk_level}</div>'
            f'<h3>{escape(t(title_key, lang))}</h3>'
            f'<p>{escape(t(body_key, lang))}</p></article>'
        )
        for risk_level, title_key, body_key in items
    )
    st.markdown(
        f"""
        <section class="ct-rules-shell">
            <div class="ct-rules-grid">{cards}</div>
            <div class="ct-review-note">
                <strong>insufficient_evidence</strong> — {escape(t('rule_insufficient_body', lang))}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_principles(lang: str) -> None:
    items = [
        ("principle_score_title", "principle_score_body"),
        ("principle_source_title", "principle_source_body"),
        ("principle_human_title", "principle_human_body"),
    ]
    content = "".join(
        (
            '<div class="ct-principle">'
            '<span class="ct-principle-dot"></span><div>'
            f"<strong>{escape(t(title_key, lang))}</strong>"
            f"<span>{escape(t(body_key, lang))}</span>"
            "</div></div>"
        )
        for title_key, body_key in items
    )
    st.markdown(
        f'<div class="ct-principles">{content}</div>',
        unsafe_allow_html=True,
    )


def render_decision_hero(
    risk_card: dict,
    llm_called: bool,
    baseline_result: dict,
    retrieval: dict | None,
    lang: str,
    has_error: bool = False,
) -> None:
    risk_level = risk_card.get("risk_level", "insufficient_evidence")
    risk_copy = RISK_TEXT.get(
        risk_level,
        RISK_TEXT["insufficient_evidence"],
    )[lang]
    action = risk_card.get("next_action")
    similarity = (
        f"{retrieval['top_score']:.4f}"
        if retrieval and retrieval.get("top_score") is not None
        else t("not_available", lang)
    )
    routed_to_human = bool(risk_card.get("abstain")) or has_error
    baseline_name = RISK_TEXT.get(
        baseline_result["risk_level"],
        RISK_TEXT["insufficient_evidence"],
    )[lang]["name"]
    meta = [
        f"{t('baseline_result', lang)} · {baseline_name}",
        f"{t('best_similarity', lang)} · {similarity}",
        f"{t('human_review', lang)} · {t('yes' if routed_to_human else 'no', lang)}",
        f"{t('human_confirmation_required', lang)} · {t('yes', lang)}",
    ]
    meta_html = "".join(
        f'<span class="ct-meta-pill">{escape(item)}</span>' for item in meta
    )
    st.markdown(
        f"""
        <div class="ct-decision {escape(risk_level)}">
            <div class="ct-decision-top">
                <span class="ct-status-icon">{escape(risk_copy['icon'])}</span>
                <div>
                    <div class="ct-decision-label">{escape(t('decision_label', lang))}</div>
                    <h2>{escape(risk_copy['name'])}</h2>
                    <div class="ct-decision-description">{escape(risk_copy['description'])}</div>
                </div>
            </div>
            {f'<div class="ct-decision-action"><strong>{escape(t("next_action", lang))}：</strong> {escape(str(action))}</div>' if action else ''}
            <div class="ct-decision-meta">{meta_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_trace_path(
    baseline_result: dict,
    retrieval: dict | None,
    llm_called: bool,
    has_error: bool,
    lang: str,
) -> None:
    baseline_name = RISK_TEXT.get(
        baseline_result["risk_level"],
        RISK_TEXT["insufficient_evidence"],
    )[lang]["name"]
    if retrieval:
        score = retrieval.get("top_score", 0.0)
        threshold = retrieval.get("threshold", 0.30)
        case_detail = t("trace_cases_detail", lang, score=f"{score:.4f}")
        threshold_detail = t(
            "trace_threshold_pass" if score >= threshold else "trace_threshold_fail",
            lang,
            score=f"{score:.4f}",
            threshold=f"{threshold:.2f}",
        )
    else:
        case_detail = t("trace_unavailable", lang)
        threshold_detail = t("trace_unavailable", lang)
    if has_error:
        decision_detail = t("trace_error", lang)
    elif llm_called:
        decision_detail = t("trace_model", lang)
    else:
        decision_detail = t("trace_human", lang)
    steps = [
        ("01", t("trace_cases", lang), case_detail),
        ("02", t("trace_threshold", lang), threshold_detail),
        ("03", t("trace_decision", lang), decision_detail),
    ]
    steps_html = "".join(
        (
            '<div class="ct-trace-step">'
            f"<small>{escape(index)}</small>"
            f"<strong>{escape(title)}</strong>"
            f"<span>{escape(detail)}</span>"
            "</div>"
        )
        for index, title, detail in steps
    )
    st.markdown(
        f"""
        <div class="ct-trace-wrap">
            <div class="ct-trace-title">{escape(t('trace_title', lang))}</div>
            <div class="ct-trace-subtitle">{escape(t('trace_help', lang))}</div>
            <div class="ct-trace-baseline">
                <strong>{escape(t('trace_baseline', lang))}：</strong>
                {escape(baseline_name)} · {escape(t('independent_baseline', lang))}
            </div>
            <div class="ct-trace-grid">{steps_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_reason_action(
    risk_card: dict,
    llm_called: bool,
    lang: str,
    has_error: bool = False,
) -> None:
    reason = risk_card.get("reason")
    action = risk_card.get("next_action")
    available = [value for value in (reason, action) if value]
    if not available:
        return
    columns = st.columns(len(available), gap="medium")
    column_index = 0
    if reason:
        with columns[column_index]:
            st.markdown(
                f"""
                <div class="ct-direct-card">
                    <div class="ct-direct-card-label">{escape(t('evidence_reason', lang))}</div>
                    <h3>{escape(t('why_this_result', lang))}</h3>
                    <p>{escape(str(reason))}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        column_index += 1
    if action:
        with columns[column_index]:
            st.markdown(
                f"""
                <div class="ct-direct-card">
                    <div class="ct-direct-card-label">{escape(t('evidence_action', lang))}</div>
                    <h3>{escape(t('what_to_do_next', lang))}</h3>
                    <p>{escape(str(action))}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

def render_case_card(case: dict, index: int, lang: str) -> None:
    title = escape(str(case.get("title") or t("none", lang)))
    case_text = escape(str(case.get("case_text") or ""))
    case_id = escape(str(case.get("case_id") or ""))
    risk_type = escape(str(case.get("risk_type") or ""))
    score = float(case.get("similarity_score") or 0.0)
    st.markdown(
        f"""
        <div class="ct-case-card">
            <div class="ct-case-rank">{escape(t('case_rank', lang, index=index))}</div>
            <h4>{title}</h4>
            <div class="ct-case-score">{escape(t('text_similarity', lang))} {score:.4f}</div>
            <p>{case_text}</p>
            <span class="ct-case-tag">{case_id} · {risk_type}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if case.get("source_url"):
        st.link_button(t("official_source", lang), case["source_url"], use_container_width=True)


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
                        f"**{t('matched_fragment', lang)}**\n\n`{match['text']}`"
                    )
                    explanation_column.markdown(
                        f"**{t('rule_explanation', lang)}**\n\n{t(_rule_key(pattern), lang)}"
                    )
                    st.caption(RISK_TEXT[risk_level][lang]["name"])


def render_empty_rule_details(lang: str) -> None:
    st.info(t("no_rule_match", lang))
    st.caption(t("no_rule_match_help", lang))


def render_sidebar(lang: str) -> None:
    with st.sidebar:
        st.markdown('<div class="ct-sidebar-brand">ClaimTrace</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ct-sidebar-status">{escape(t("sidebar_status", lang))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"### {t('sidebar_guide', lang)}")
        legend_items = [
            ("high_risk", "rule_high_title", "!"),
            ("evidence_needed", "rule_evidence_title", "◆"),
            ("low_risk", "rule_low_title", "○"),
            ("insufficient_evidence", "rule_insufficient_title", "→"),
        ]
        legend_html = "".join(
            (
                f'<div class="ct-legend-row {tone}">'
                f'<span class="ct-legend-icon">{icon}</span>'
                f"<strong>{escape(t(label_key, lang))}</strong></div>"
            )
            for tone, label_key, icon in legend_items
        )
        st.markdown(f'<div class="ct-sidebar-legend">{legend_html}</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown(f"### {t('sidebar_limits', lang)}")
        limits = [t("limit_cases", lang), t("limit_threshold", lang), t("limit_human", lang)]
        st.markdown(
            '<div class="ct-sidebar-boundary">'
            + "".join(f"• {escape(item)}<br>" for item in limits)
            + "</div>",
            unsafe_allow_html=True,
        )
