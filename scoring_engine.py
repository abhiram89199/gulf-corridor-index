"""
Gulf Corridor Index (GCI) - Scoring Engine
============================================
This file contains the actual decision logic: turning the raw route_data.py
numbers into a ranked recommendation based on what the user cares about.

Kept separate from app.py (the UI) so the math is easy to test and easy
to explain to someone who asks "how does this actually work?"
"""

from route_data import ROUTES, PRIORITY_WEIGHTS


def calculate_total_cost(route_key: str) -> float:
    """Returns the estimated total cost per container, including crisis surcharge."""
    route = ROUTES[route_key]
    base = route["base_cost_usd"]
    surcharge = base * (route["crisis_surcharge_pct"] / 100)
    return round(base + surcharge, 2)


def calculate_avg_transit_days(route_key: str) -> float:
    """Returns the midpoint of the transit day range for a route."""
    low, high = ROUTES[route_key]["transit_days"]
    return round((low + high) / 2, 1)


def normalize(value: float, all_values: list[float], lower_is_better: bool = True) -> float:
    """
    Converts a raw number (cost, days, or risk) into a 0-100 score
    relative to the other routes being compared, so cost/time/risk
    can be fairly combined even though they're on totally different scales.

    A score of 100 = best in the group, 0 = worst in the group.
    """
    if not all_values or max(all_values) == min(all_values):
        return 100.0  # all routes equal on this dimension

    min_v, max_v = min(all_values), max(all_values)
    if lower_is_better:
        return round(100 * (max_v - value) / (max_v - min_v), 1)
    else:
        return round(100 * (value - min_v) / (max_v - min_v), 1)


def rank_routes(priority: str) -> list[dict]:
    """
    Main function the app calls. Returns all 6 routes ranked best-to-worst
    for the given priority ('cost', 'time', or 'safety').

    Each returned dict has the raw numbers (for display) AND the composite
    score (for ranking), so the UI can show both "here's the real cost"
    and "here's why we ranked it this way."
    """
    if priority not in PRIORITY_WEIGHTS:
        raise ValueError(f"Unknown priority '{priority}'. Use 'cost', 'time', or 'safety'.")

    weights = PRIORITY_WEIGHTS[priority]

    # Step 1: gather raw numbers for every route
    raw = {}
    for key in ROUTES:
        raw[key] = {
            "cost": calculate_total_cost(key),
            "time": calculate_avg_transit_days(key),
            "risk": ROUTES[key]["risk_score"],
        }

    all_costs = [v["cost"] for v in raw.values()]
    all_times = [v["time"] for v in raw.values()]
    all_risks = [v["risk"] for v in raw.values()]

    # Step 2: normalize each dimension 0-100 (lower cost/time/risk = better)
    results = []
    for key, route in ROUTES.items():
        cost_score = normalize(raw[key]["cost"], all_costs, lower_is_better=True)
        time_score = normalize(raw[key]["time"], all_times, lower_is_better=True)
        risk_score = normalize(raw[key]["risk"], all_risks, lower_is_better=True)

        composite = (
            cost_score * weights["cost"]
            + time_score * weights["time"]
            + risk_score * weights["risk"]
        )

        results.append({
            "route_key": key,
            "display_name": route["display_name"],
            "description": route["description"],
            "total_cost_usd": raw[key]["cost"],
            "avg_transit_days": raw[key]["time"],
            "transit_days_range": route["transit_days"],
            "risk_score": route["risk_score"],
            "strait_exposure": route["strait_exposure"],
            "notes": route["notes"],
            "source": route["source"],
            "composite_score": round(composite, 1),
        })

    # Step 3: sort best to worst
    results.sort(key=lambda r: r["composite_score"], reverse=True)
    return results


def get_recommendation_summary(priority: str) -> dict:
    """Returns the top-ranked route plus a one-line plain-English reason why."""
    ranked = rank_routes(priority)
    top = ranked[0]

    reason_map = {
        "cost": f"Lowest effective cost per container at ${top['total_cost_usd']:,.0f}, factoring in current crisis surcharges.",
        "time": f"Fastest realistic transit at roughly {top['avg_transit_days']} days.",
        "safety": f"Lowest risk exposure (risk score {top['risk_score']}/100), avoiding the Strait entirely." if not top["strait_exposure"] else f"Best available option, though it still carries Strait exposure.",
    }

    return {
        "route": top,
        "reason": reason_map.get(priority, ""),
        "full_ranking": ranked,
    }
