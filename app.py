"""
Gulf Corridor Index (GCI) - Light Theme
============================================
A maritime-intelligence decision tool that scores 6 Gulf shipping routes
against current Hormuz crisis conditions and recommends the best route
based on what matters most: cost, time, or safety.

Built by Sai Abhiram Manoj Kalluri
MBA Candidate, Supply Chain & Global Operations, Middlesex University Dubai
"""

import streamlit as st
import base64
from pathlib import Path
from route_data import (
    GCI_CURRENT_SCORE, GCI_STATUS_LABEL, GCI_LAST_UPDATED,
    GCI_SOURCE_NOTE, GCI_HISTORY, ROUTES,
)
from scoring_engine import rank_routes, get_recommendation_summary

st.set_page_config(
    page_title="Gulf Corridor Index",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def _load_b64(filename):
    try:
        return base64.b64encode((Path(__file__).parent / filename).read_bytes()).decode()
    except Exception:
        return ""

BG_B64 = _load_b64("logistics_bg.png")

# ── LIGHT THEME STYLING ───────────────────────────────────────────
# Pale logistics background, dark navy text, soft white cards.
# Space Grotesk display, Inter body, IBM Plex Mono for data figures.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

.stApp {
    background-image:
        linear-gradient(180deg, rgba(244,248,252,0.55) 0%, rgba(238,244,250,0.80) 100%),
        url("data:image/png;base64,BG_B64_PLACEHOLDER");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    color: #15293D;
}
.block-container {
    padding-top: 2.5rem;
    max-width: 1100px;
}
#MainMenu, footer, header {visibility: hidden;}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #15293D;
}

/* Masthead */
.gci-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #B26B16;
    margin-bottom: 0.5rem;
}
.gci-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.4rem;
    font-weight: 700;
    color: #0E2138;
    line-height: 1.02;
    letter-spacing: -0.01em;
    margin: 0;
}
.gci-sub {
    font-size: 0.98rem;
    color: #4A6178;
    margin-top: 0.6rem;
    max-width: 620px;
}
.gci-rule {
    height: 1px;
    background: linear-gradient(90deg, #D98A2B 0%, #C9D6E3 35%, #C9D6E3 100%);
    border: none;
    margin: 1.8rem 0;
}

/* Index readout card */
.gci-index-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid #D4E0EC;
    border-left: 3px solid #D98A2B;
    border-radius: 6px;
    padding: 1.5rem 1.6rem;
    box-shadow: 0 2px 14px rgba(20,41,61,0.06);
}
.gci-index-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #6B8198;
}
.gci-index-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 4.2rem;
    font-weight: 600;
    line-height: 1;
    margin: 0.4rem 0 0.2rem 0;
}
.gci-index-max {
    font-size: 1.6rem;
    color: #A9BACB;
}
.gci-status {
    font-size: 0.95rem;
    font-weight: 600;
    margin-top: 0.4rem;
}
.gci-updated {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #7E91A6;
    margin-top: 0.7rem;
}

/* Section headers */
.gci-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #B26B16;
    margin: 0.5rem 0 0.2rem 0;
}

/* Recommendation banner */
.gci-reco {
    background: rgba(240,250,244,0.9);
    border: 1px solid #B7DEC8;
    border-left: 3px solid #2FA86C;
    border-radius: 6px;
    padding: 1.1rem 1.3rem;
    margin-top: 0.4rem;
    box-shadow: 0 2px 14px rgba(20,41,61,0.05);
}
.gci-reco-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #2FA86C;
}
.gci-reco-route {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.45rem;
    font-weight: 600;
    color: #0E2138;
    margin: 0.2rem 0;
}
.gci-reco-reason {
    font-size: 0.9rem;
    color: #3E556C;
}

.stRadio label, .stSelectbox label {
    color: #3E556C !important;
    font-size: 0.9rem !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #D4E0EC;
    border-radius: 6px;
    background: rgba(255,255,255,0.75);
}

.gci-footer {
    font-size: 0.76rem;
    color: #6B8198;
    line-height: 1.6;
    border-top: 1px solid #D4E0EC;
    padding-top: 1.2rem;
    margin-top: 2.5rem;
}
.gci-method {
    font-size: 0.82rem;
    color: #4A6178;
    line-height: 1.6;
}
</style>
""".replace("BG_B64_PLACEHOLDER", BG_B64), unsafe_allow_html=True)

# ── MASTHEAD ──────────────────────────────────────────────────────
st.markdown("""
<div class="gci-eyebrow">Hormuz Crisis Intelligence &middot; Day 109</div>
<h1 class="gci-title">Gulf Corridor Index</h1>
<p class="gci-sub">A risk-adjusted benchmark and route decision tool for Gulf shipping during the 2026 Strait of Hormuz disruption. Every figure is sourced, dated, and labeled for confidence.</p>
""", unsafe_allow_html=True)
st.markdown('<hr class="gci-rule">', unsafe_allow_html=True)

# ── TOP SECTION ───────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.25], gap="large")

with col_left:
    if GCI_CURRENT_SCORE >= 75:
        val_color = "#D33A3F"
    elif GCI_CURRENT_SCORE >= 50:
        val_color = "#C77B1E"
    else:
        val_color = "#2FA86C"

    st.markdown(f"""
    <div class="gci-index-card">
        <div class="gci-index-label">Current Index Reading</div>
        <div class="gci-index-value" style="color:{val_color};">{GCI_CURRENT_SCORE}<span class="gci-index-max"> / 100</span></div>
        <div class="gci-status" style="color:{val_color};">{GCI_STATUS_LABEL}</div>
        <div class="gci-updated">Updated {GCI_LAST_UPDATED.strftime('%d %b %Y').upper()}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gci-section" style="margin-top:1.4rem;">Index Trend</div>', unsafe_allow_html=True)
    trend_data = {str(h["date"]): h["score"] for h in GCI_HISTORY}
    st.line_chart(trend_data, height=180, color="#C77B1E")

    with st.expander("How is this index calculated?"):
        st.markdown(f'<div class="gci-method">{GCI_SOURCE_NOTE}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="gci-method" style="margin-top:0.6rem;">This is a manually curated benchmark, not a live data feed. '
            'It is refreshed weekly from public crisis reporting (vessel transit counts, carrier advisories, mine clearance status). '
            'Every number can be traced to a dated source.</div>',
            unsafe_allow_html=True,
        )

with col_right:
    st.markdown('<div class="gci-section">Route Decision</div>', unsafe_allow_html=True)

    priority = st.radio(
        "What matters most for this shipment?",
        options=["cost", "time", "safety"],
        format_func=lambda x: {"cost": "Lowest cost", "time": "Fastest transit", "safety": "Lowest risk"}[x],
        horizontal=True,
    )

    cargo_type = st.selectbox(
        "Cargo profile (context only, does not change scoring)",
        ["General cargo", "Perishables / time-sensitive", "High-value goods", "Bulk / non-urgent"],
    )

    summary = get_recommendation_summary(priority)
    top_route = summary["route"]

    st.markdown(f"""
    <div class="gci-reco">
        <div class="gci-reco-label">Recommended Route</div>
        <div class="gci-reco-route">{top_route['display_name']}</div>
        <div class="gci-reco-reason">{summary['reason']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="gci-rule">', unsafe_allow_html=True)

# ── FULL COMPARISON TABLE ─────────────────────────────────────────
st.markdown('<div class="gci-section">All Six Routes, Ranked</div>', unsafe_allow_html=True)

ranked = rank_routes(priority)

table_data = []
for r in ranked:
    confidence = ROUTES[r["route_key"]].get("confidence", "estimated")
    table_data.append({
        "Route": r["display_name"],
        "Est. cost / container": f"${r['total_cost_usd']:,.0f}",
        "Transit": f"{r['transit_days_range'][0]}-{r['transit_days_range'][1]} days",
        "Risk": f"{r['risk_score']}/100",
        "Strait": "Yes" if r["strait_exposure"] else "No",
        "Data confidence": "Confirmed" if confidence == "confirmed" else "Estimated",
        "Match": r['composite_score'],
    })

st.dataframe(
    table_data,
    width="stretch",
    hide_index=True,
    column_config={
        "Match": st.column_config.ProgressColumn(
            "Match score", min_value=0, max_value=100, format="%.1f",
        ),
    },
)

st.markdown(
    '<div class="gci-method" style="margin-top:0.3rem;">Routes are labeled <b>Confirmed</b> (a specific named source backs this route\'s figures) '
    'or <b>Estimated</b> (built from general industry surcharge patterns, not a route-specific published rate). '
    'This distinction is deliberate. Transparency outranks false precision.</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="gci-section" style="margin-top:1.6rem;">Route Notes</div>', unsafe_allow_html=True)
for r in ranked:
    confidence = ROUTES[r["route_key"]].get("confidence", "estimated")
    tag = "Confirmed" if confidence == "confirmed" else "Estimated"
    with st.expander(f"{r['display_name']}  ·  {tag}"):
        st.markdown(f'<div class="gci-method">{r["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="gci-updated">Source: {r["source"]}</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("""
<div class="gci-footer">
The Gulf Corridor Index is an independent research project on Gulf supply chain resilience during the 2026 Strait of Hormuz disruption.
Figures are manually curated from public sources and refreshed weekly. Not affiliated with any carrier, port authority, or logistics company.
<br><br>
Built by <b>Sai Abhiram Manoj Kalluri</b> &middot; MBA Candidate, Supply Chain &amp; Global Operations &middot; Middlesex University Dubai
</div>
""", unsafe_allow_html=True)
