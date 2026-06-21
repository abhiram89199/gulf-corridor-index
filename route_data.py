"""
Gulf Corridor Index (GCI) - Route Database
============================================
This file holds every editable number in the tool. As crisis conditions
change week to week, this is the ONLY file you should need to touch.

Each route has:
  - base_cost_usd: cost per 40ft container (FEU) at baseline, before crisis surcharges
  - crisis_surcharge_pct: extra cost % being added right now because of Hormuz conditions
  - transit_days: (min, max) typical sailing/transit time in days
  - risk_score: 0-100, how exposed this specific route is to Hormuz/regional risk (0=safest)
  - strait_exposure: True if this route physically passes through the Strait of Hormuz
  - notes: short, source-backed description of why the numbers are what they are
  - source: where the underlying figures came from (for transparency)
  - confidence: "confirmed" or "estimated" — see below, this matters a lot

CONFIDENCE LEVELS, READ THIS BEFORE QUOTING ANY NUMBER TO SOMEONE:
  "confirmed" = cost/surcharge figures are backed by a specific, named,
      datable industry source (a named report, carrier advisory, or
      named outlet). You can defend these numbers if challenged.
  "estimated" = built from general industry surcharge patterns (typical
      war-risk premiums, typical feeder rate behavior) rather than a
      source naming THIS specific route's exact dollar figures. Still
      directionally reasonable, but say "estimated" out loud if asked,
      don't present these as confirmed facts.

Right now: hormuz_direct and cape_of_good_hope are "confirmed".
khor_fakkan_feeder, salalah_transhipment, and jeddah_land_bridge are
"estimated". air_freight is "estimated" (general air surge reporting,
not this specific route). Upgrade these to "confirmed" only when you
find a specific source for that exact route's numbers.

IMPORTANT: crisis_surcharge_pct and risk_score should be reviewed weekly.
See UPDATE_LOG at the bottom for instructions on how to refresh these.
"""

from datetime import date

# ── GULF CORRIDOR INDEX (GCI) — overall crisis pressure score ──────────────
# This is the headline number shown at the top of the app.
# Scale: 0 = normal pre-crisis conditions, 100 = total operational paralysis
GCI_CURRENT_SCORE = 92
GCI_STATUS_LABEL = "Extreme — active blockade, near-zero transits"
GCI_LAST_UPDATED = date(2026, 6, 17)
GCI_SOURCE_NOTE = (
    "Based on IMF PortWatch vessel transit counts (0 outbound transits "
    "recorded June 14, 2026, vs ~94/day pre-crisis baseline) and BIMCO "
    "operational risk commentary. Re-verified via live search on June 17, "
    "2026: strait remains effectively closed to commercial shipping despite "
    "the US-Iran MOU signed June 15-16, since mine clearance is estimated "
    "to take 40-50 days and both sides are still enforcing blockades on "
    "the water. Update this weekly from public crisis reporting."
)

# Historical GCI scores for trend context (used in the small trend line in the UI)
GCI_HISTORY = [
    {"date": date(2026, 3, 1), "score": 78, "label": "Initial Hormuz disruption begins"},
    {"date": date(2026, 4, 1), "score": 85, "label": "Carriers suspend Hormuz transit"},
    {"date": date(2026, 5, 1), "score": 88, "label": "Maersk Operational Update period"},
    {"date": date(2026, 6, 1), "score": 90, "label": "OPEC+ confirms extended disruption"},
    {"date": date(2026, 6, 13), "score": 94, "label": "Zero transit days recorded"},
    {"date": date(2026, 6, 17), "score": 92, "label": "MOU signed, operational reality lags"},
]

# ── ROUTE DATABASE ───────────────────────────────────────────────────────
# 6 routes companies are actually choosing between right now.

ROUTES = {
    "hormuz_direct": {
        "display_name": "Hormuz Direct",
        "description": "The normal pre-crisis route through the Strait of Hormuz itself.",
        "base_cost_usd": 3000,
        "crisis_surcharge_pct": 45,
        "transit_days": (18, 22),
        "risk_score": 95,
        "strait_exposure": True,
        "notes": (
            "Technically still the shortest path, but carriers are not running "
            "normal schedules through it. Active naval presence and mine "
            "clearance operations make this the highest-risk option even "
            "after the June MOU was signed."
        ),
        "source": "BIMCO commentary, June 2026; IMF PortWatch transit data",
        "confidence": "confirmed",
    },
    "khor_fakkan_feeder": {
        "display_name": "Khor Fakkan Feeder",
        "description": "UAE east coast port, outside the Strait entirely.",
        "base_cost_usd": 3200,
        "crisis_surcharge_pct": 20,
        "transit_days": (20, 24),
        "risk_score": 35,
        "strait_exposure": False,
        "notes": (
            "Feeder operations from UAE's Gulf of Oman coast bypass the Strait "
            "chokepoint. Capacity constrained because many companies are "
            "trying to use this route simultaneously, which is pushing up "
            "feeder rates."
        ),
        "source": "Estimated from general Gulf feeder/transhipment surcharge patterns. No route-specific published rate found yet.",
        "confidence": "estimated",
    },
    "salalah_transhipment": {
        "display_name": "Salalah Transhipment",
        "description": "Oman's deep-water port, also outside the Strait.",
        "base_cost_usd": 3400,
        "crisis_surcharge_pct": 25,
        "transit_days": (22, 27),
        "risk_score": 30,
        "strait_exposure": False,
        "notes": (
            "Similar profile to Khor Fakkan. Salalah has more transhipment "
            "capacity but adds extra days for cargo transfer."
        ),
        "source": "Estimated from general Gulf feeder/transhipment surcharge patterns. No route-specific published rate found yet.",
        "confidence": "estimated",
    },
    "jeddah_land_bridge": {
        "display_name": "Jeddah Land Bridge",
        "description": "Sea to Red Sea side via Saudi land crossing.",
        "base_cost_usd": 3800,
        "crisis_surcharge_pct": 30,
        "transit_days": (24, 30),
        "risk_score": 40,
        "strait_exposure": False,
        "notes": (
            "Avoids Hormuz but still touches Red Sea routing, which carries "
            "its own separate Houthi-related risk. Land bridge adds "
            "trucking cost and customs handling time."
        ),
        "source": "Estimated by combining general Red Sea crisis surcharge reporting with land-bridge handling cost assumptions. No single source confirms this exact route's pricing.",
        "confidence": "estimated",
    },
    "cape_of_good_hope": {
        "display_name": "Cape of Good Hope",
        "description": "The long way around Africa, avoiding both Hormuz and the Red Sea.",
        "base_cost_usd": 3000,
        "crisis_surcharge_pct": 40,
        "transit_days": (10, 14),  # ADDED transit days, not total
        "transit_days_note": "10-14 additional days on top of the normal route, not total transit time",
        "risk_score": 15,
        "strait_exposure": False,
        "notes": (
            "Adds 10-14 days and roughly 30-50% cost increase on key lanes. "
            "War-risk and conflict surcharges of $200-800 per container have "
            "become standard line items. Safest option by far, but slowest "
            "and most expensive for time-sensitive cargo."
        ),
        "source": "Maritime Gateway, March 2026; multiple carrier advisories (Maersk, Hapag-Lloyd, CMA CGM); confirmed again via June 2026 search (30-50% surcharge, 10-14 day addition, $200-800 war-risk surcharge per container)",
        "confidence": "confirmed",
    },
    "air_freight": {
        "display_name": "Air Freight",
        "description": "Fastest option, zero Strait exposure, premium cost.",
        "base_cost_usd": 9500,
        "crisis_surcharge_pct": 60,
        "transit_days": (2, 5),
        "risk_score": 5,
        "strait_exposure": False,
        "notes": (
            "Reserved for high-value or time-critical cargo given the cost "
            "multiple versus ocean freight. Air rates have surged "
            "significantly on Gulf-adjacent lanes during the crisis."
        ),
        "source": "Maritime Gateway, March 2026 (general air rate surge reporting on Gulf-adjacent lanes, not this exact route's published rate)",
        "confidence": "estimated",
    },
}

# ── PRIORITY WEIGHTING ──────────────────────────────────────────────────
# When a user picks a priority, these weights decide how routes are ranked.
# Each weight should sum to 1.0 across cost/time/risk.
PRIORITY_WEIGHTS = {
    "cost": {"cost": 0.6, "time": 0.2, "risk": 0.2},
    "time": {"cost": 0.2, "time": 0.6, "risk": 0.2},
    "safety": {"cost": 0.15, "time": 0.15, "risk": 0.7},
}

# ── UPDATE LOG ────────────────────────────────────────────────────────
# How to refresh this file weekly (takes about 10-15 minutes):
#
# 1. Search: "Strait of Hormuz vessel transits this week"
#    Update GCI_CURRENT_SCORE and GCI_STATUS_LABEL based on what you find.
#    Add a new entry to GCI_HISTORY.
#
# 2. Search: "[route name] shipping cost surcharge 2026" for each route
#    Update crisis_surcharge_pct if rates have moved meaningfully.
#
# 3. Search: "Strait of Hormuz mine clearance" or "Hormuz blockade status"
#    Update risk_score for hormuz_direct based on current operational status.
#
# 4. Update GCI_LAST_UPDATED to today's date.
#
# Keep a copy of search sources in your notes so you can defend any number
# if someone like Hussein asks where it came from.
