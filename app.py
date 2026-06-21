"""
Gulf Corridor Index (GCI)
============================================
A maritime-intelligence style decision tool that scores 6 Gulf shipping
routes against current Hormuz crisis conditions and recommends the best
route based on what matters most: cost, time, or safety.

Built by Sai Abhiram Manoj Kalluri
MBA Candidate, Supply Chain & Global Operations, Middlesex University Dubai

To run locally:
    streamlit run app.py
"""

import streamlit as st
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

# ── PROFESSIONAL STYLING ──────────────────────────────────────────
# Maritime intelligence aesthetic: deep navy, amber signal accent,
# monospace data figures the way real shipping indices display.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap');

/* App background and base */
.stApp {
    background: #0B1622;
    color: #C9D6E3;
}
.block-container {
    padding-top: 2.5rem;
    max-width: 1100px;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}

/* Typography */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Masthead */
.gci-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #E8A33D;
    margin-bottom: 0.5rem;
}
.gci-title {
    font-family: 'Fraunces', serif;
    font-size: 2.9rem;
    font-weight: 600;
    color: #F4F8FC;
    line-height: 1.05;
    margin: 0;
}
.gci-sub {
    font-size: 0.98rem;
    color: #7E91A6;
    margin-top: 0.6rem;
    max-width: 620px;
}
.gci-rule {
    height: 1px;
    background: linear-gradient(90deg, #E8A33D 0%, #1E3048 35%, #1E3048 100%);
    border: none;
    margin: 1.8rem 0;
}

/* Index readout card */
.gci-index-card {
    background: #0F1E2E;
    border: 1px solid #1E3048;
    border-left: 3px solid #E8A33D;
    border-radius: 4px;
    padding: 1.5rem 1.6rem;
}
.gci-index-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #7E91A6;
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
    color: #45586D;
}
.gci-status {
    font-size: 0.95rem;
    font-weight: 600;
    margin-top: 0.4rem;
}
.gci-updated {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #5C7088;
    margin-top: 0.7rem;
}

/* Section headers */
.gci-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #E8A33D;
    margin: 0.5rem 0 0.2rem 0;
}

/* Recommendation banner */
.gci-reco {
    background: #112436;
    border: 1px solid #214A38;
    border-left: 3px solid #4CC38A;
    border-radius: 4px;
    padding: 1.1rem 1.3rem;
    margin-top: 0.4rem;
}
.gci-reco-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4CC38A;
}
.gci-reco-route {
    font-size: 1.35rem;
    font-weight: 700;
    color: #F4F8FC;
    margin: 0.2rem 0;
}
.gci-reco-reason {
    font-size: 0.9rem;
    color: #A9BACB;
}

/* Radio + select labels */
.stRadio label, .stSelectbox label {
    color: #A9BACB !important;
    font-size: 0.9rem !important;
}

/* Dataframe tweaks */
[data-testid="stDataFrame"] {
    border: 1px solid #1E3048;
    border-radius: 4px;
}

/* Expander */
.streamlit-expanderHeader {
    background: #0F1E2E;
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Footer note */
.gci-footer {
    font-size: 0.76rem;
    color: #5C7088;
    line-height: 1.6;
    border-top: 1px solid #1E3048;
    padding-top: 1.2rem;
    margin-top: 2.5rem;
}
.gci-method {
    font-size: 0.82rem;
    color: #7E91A6;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ──────────────────────────────────────────────────────
st.markdown('<div class="gci-eyebrow">Hormuz Crisis Intelligence &middot; Day 109</div>', unsafe_allow_html=True)
st.markdown('<h1 class="gci-title">Gulf Corridor Index</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="gci-sub">A risk-adjusted benchmark and route decision tool for Gulf shipping during the 2026 Strait of Hormuz disruption. Every figure is sourced, dated, and labeled for confidence.</p>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="gci-rule">', unsafe_allow_html=True)

# ── TOP SECTION ───────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.25], gap="large")

with col_left:
    # Color logic for the index value
    if GCI_CURRENT_SCORE >= 75:
        val_color = "#E5484D"
    elif GCI_CURRENT_SCORE >= 50:
        val_color = "#E8A33D"
    else:
        val_color = "#4CC38A"

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
    st.line_chart(trend_data, height=180, color="#E8A33D")

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
            "Match score",
            min_value=0,
            max_value=100,
            format="%.1f",
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
