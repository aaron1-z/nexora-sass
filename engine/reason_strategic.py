"""
Strategic reasoning with LLM (FAST REFINEMENT) + rule-based core
(<2 MIN SAFE VERSION)
"""

from typing import List, Dict, Any
from statistics import mean
from collections import Counter

from .utils import log, parse_json_loose


# --------------------------------------------------
# CONFIG (CRITICAL)
# --------------------------------------------------

MAX_LLM_ARTICLES = 6           # 👈 HARD CAP
MAX_LLM_TOKENS = 280           # Short outputs only
LLM_SENTIMENT_TRIGGER = 0.2    # Only refine when signal is strong


# --------------------------------------------------
# Global reasoner (lazy, safe)
# --------------------------------------------------

_REASONER = None


def _load_reasoner():
    global _REASONER
    if _REASONER is not None:
        return _REASONER

    try:
        from transformers import pipeline
        log.info("Loading strategic reasoner (flan-t5-base)...")

        _REASONER = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1,
        )

        log.info("Reasoner loaded successfully")
        return _REASONER

    except Exception as e:
        log.warning(f"Failed to load reasoner model: {e}")
        return None


# --------------------------------------------------
# Rule-based core (PRIMARY)
# --------------------------------------------------

def _rule_based_brief(
    query: str,
    analyzed: List[Dict[str, Any]],
    historical: List[Dict[str, Any]],
) -> Dict[str, Any]:

    all_catalysts, all_entities, sentiments = [], [], []

    for it in analyzed:
        all_catalysts.extend(it.get("catalysts", []))
        all_entities.extend(it.get("entities", []))
        sentiments.append(it.get("sentiment", 0.0))

    top_catalysts = [c for c, _ in Counter(all_catalysts).most_common(5)]
    top_entities = [e for e, _ in Counter(all_entities).most_common(5)]
    avg_sent = mean(sentiments) if sentiments else 0.0

    # Sector mapping
    q = query.lower()
    if "nvidia" in q:
        sector = "AI chips and data centers"
    elif "tesla" in q:
        sector = "electric vehicles and autonomy"
    elif "quantum" in q:
        sector = "quantum computing hardware"
    else:
        sector = "technology and markets"

    # Scenario weights
    if avg_sent > 0.15:
        bull, base, bear = 40, 35, 25
    elif avg_sent < -0.15:
        bull, base, bear = 25, 35, 40
    else:
        bull, base, bear = 30, 40, 30

    total = bull + base + bear
    scenarios = [
        {
            "name": "Bull",
            "prob": int(bull * 100 / total),
            "path": [
                f"Momentum improves across {sector}",
                "Key catalysts resolve positively",
                "Execution exceeds expectations",
            ],
            "signals": ["Positive sentiment trend", "Catalyst confirmation"],
        },
        {
            "name": "Base",
            "prob": int(base * 100 / total),
            "path": [
                "Mixed signals persist",
                "Market digests developments",
                "Range-bound outcomes",
            ],
            "signals": ["Neutral sentiment", "Balanced news flow"],
        },
        {
            "name": "Bear",
            "prob": 100 - int(bull * 100 / total) - int(base * 100 / total),
            "path": [
                "Negative catalysts dominate",
                "Execution or policy risks rise",
                "Risk repricing accelerates",
            ],
            "signals": ["Sentiment deterioration", "Downside catalysts"],
        },
    ]

    actions = [
        {
            "title": f"Monitor {query} closely",
            "rationale": f"{len(analyzed)} recent signals with avg sentiment {avg_sent:+.2f}.",
            "steps": [
                "Track dominant catalysts",
                "Watch sentiment inflection points",
                "Reassess weekly",
            ],
            "impact_score": 3 + int(abs(avg_sent) > 0.3),
        },
        {
            "title": "Assess exposure to key entities",
            "rationale": "Entity behavior drives second-order effects.",
            "steps": [
                "Track top entity mentions",
                "Compare sentiment divergence",
            ],
            "impact_score": 2,
        },
    ]

    triggers = [
        f"IF sentiment > {avg_sent + 0.3:+.2f} THEN increase exposure",
        f"IF sentiment < {avg_sent - 0.3:+.2f} THEN reduce exposure",
        f"IF '{top_catalysts[0] if top_catalysts else 'Regulatory'}' spikes THEN reassess",
        "IF multiple downside catalysts align THEN escalate review",
    ]

    confidence = "High" if len(analyzed) >= 12 else "Medium"

    return {
        "executive_summary": (
            f"{len(analyzed)} developments in '{query}' show avg sentiment {avg_sent:+.2f}. "
            f"Key drivers include {', '.join(top_catalysts[:3] or ['general trends'])}."
        ),
        "immediate_impact": (
            f"Near-term outlook is "
            f"{'positive' if avg_sent > 0 else 'negative' if avg_sent < 0 else 'neutral'} "
            f"with moderate volatility."
        ),
        "scenarios": scenarios,
        "actions": actions,
        "watch_triggers": triggers,
        "confidence": confidence,
    }


# --------------------------------------------------
# Strategic reasoning (REFINEMENT ONLY)
# --------------------------------------------------

def strategic_reason(
    query: str,
    analyzed: List[Dict[str, Any]],
    historical: List[Dict[str, Any]],
) -> Dict[str, Any]:

    fallback = _rule_based_brief(query, analyzed, historical)

    avg_sent = mean([a.get("sentiment", 0) for a in analyzed]) if analyzed else 0

    # 👇 Skip LLM unless signal is meaningful
    if abs(avg_sent) < LLM_SENTIMENT_TRIGGER:
        return fallback

    reasoner = _load_reasoner()
    if reasoner is None:
        return fallback

    try:
        bullets = []
        for it in analyzed[:MAX_LLM_ARTICLES]:
            bullets.append(
                f"- {it.get('title','')}: {it.get('summary','')[:140]}"
            )

        prompt = f"""
You are refining an existing strategic brief.

TOPIC: {query}

SIGNALS:
{chr(10).join(bullets)}

TASK:
Improve clarity and specificity of:
- executive_summary
- immediate_impact
- watch_triggers

Return ONLY valid JSON with these keys.
"""

        out = reasoner(prompt, max_new_tokens=MAX_LLM_TOKENS, do_sample=False)
        data = parse_json_loose(out[0]["generated_text"]) or {}

        for key in fallback:
            if key not in data or not data[key]:
                data[key] = fallback[key]

        return data

    except Exception as e:
        log.error(f"LLM refinement failed: {e}")
        return fallback
