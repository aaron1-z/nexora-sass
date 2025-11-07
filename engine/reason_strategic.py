from typing import List, Dict, Any, Tuple
from transformers import pipeline
import os, json
from statistics import mean

from .utils import MODELS_DIR, parse_json_loose, score_confidence, clean_text, log


def _load_reasoner():
    """
    Load a light, CPU-safe text2text model.
    We keep device on CPU for reliability; flan-t5-small/base are fast.
    """
    candidates = [
        os.environ.get("NEXORA_STRATEGY_MODEL"),
        "google/flan-t5-base",
        "google/flan-t5-small",
    ]
    candidates = [c for c in candidates if c]
    last_err = None
    for name in candidates:
        try:
            log.info(f"Loading strategic reasoner: {name}")
            p = pipeline(
                "text2text-generation",
                model=name,
                tokenizer=name,
                device=-1,
                max_length=768,
                truncation=True,
                cache_dir=MODELS_DIR,
            )
            log.info("Reasoner ready")
            return p
        except Exception as e:
            last_err = e
            log.warning("Strategic model load failed for %s: %s", name, e)
    raise RuntimeError(f"Failed to load strategic model: {last_err}")


_REASONER = _load_reasoner()


def _top(items: List[Dict[str, Any]], key: str, n: int) -> List[str]:
    counts: Dict[str, int] = {}
    for it in items or []:
        for v in it.get(key) or []:
            counts[v] = counts.get(v, 0) + 1
    return [k for k, _ in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]]


def _stats(items: List[Dict[str, Any]]) -> Tuple[float, float]:
    sents = [float(x.get("sentiment", 0.0)) for x in items or [] if x is not None]
    return (mean(sents) if sents else 0.0, max(sents) if sents else 0.0)


def _build_prompt(query: str, new_events: List[Dict[str, Any]], historical: List[Dict[str, Any]]) -> str:
    """Compose a compact but information-dense prompt for the model."""
    def line(ev: Dict[str, Any]) -> str:
        cats = ", ".join(ev.get("catalysts", [])[:4])
        return f"- {ev.get('title','')[:160]} [cats: {cats}]"

    new_lines = "\n".join([line(e) for e in new_events[:10]]) or "- (none)"
    hist_lines = "\n".join([line(h) for h in historical[:6]]) or "- (none)"

    schema = {
        "executive_summary": "2–4 sentences",
        "immediate_impact": "2 sentences on liquidity/flows/sentiment",
        "scenarios": [
            {"name": "Bull", "prob": 0-100, "path": "2-3 bullet narrative", "signals": ["leading indicator", "threshold"]},
            {"name": "Base", "prob": 0-100, "path": "…", "signals": []},
            {"name": "Bear", "prob": 0-100, "path": "…", "signals": []},
        ],
        "actions": [
            {"title":"Hedge or Tactical", "rationale":"…", "steps":["…","…"], "sizing":"% or units", "kpis":["metric","metric"], "timeline":"T+7/T+30 milestones", "risks":["risk","risk"], "mitigations":["…"]},
            {"title":"Core Position", "rationale":"…", "steps":[ ], "sizing":"…", "kpis":[ ], "timeline":"…", "risks":[ ], "mitigations":[ ]},
        ],
        "watch_triggers": ["event → action", "threshold → action"],
        "confidence": "High/Medium/Low"
    }

    return f"""
You are Nexora — a professional markets/strategy analyst.

Focus: "{query}"

Recent events:
{new_lines}

Historical analogs:
{hist_lines}

Task:
1) Synthesize a decision-grade brief.
2) Include a 3-scenario tree (Bull/Base/Bear) with probabilities (sum≈100) and leading signals.
3) Produce 3–6 concrete actions with steps, sizing guidance, KPIs to monitor, timelines, key risks and mitigations.
4) Provide 4–8 watch triggers (IF/THEN rules).
5) Confidence: High/Medium/Low.
Return ONLY JSON exactly matching this schema:
{json.dumps(schema, ensure_ascii=False, indent=2)}
No prose outside JSON.
""".strip()


def _safe_json(text: str) -> Dict[str, Any]:
    try:
        return parse_json_loose(text)
    except Exception:
        return {}


def _rule_based_brief(query: str, analyzed: List[Dict[str, Any]], historical: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    When model output is weak or malformed, synthesize a structured brief from heuristics.
    """
    top_cats = _top(analyzed, "catalysts", 6)
    avg_sent, max_sent = _stats(analyzed)

    # scenario probabilities based on sentiment tilt
    tilt = avg_sent
    bull = max(10, int(35 + 40 * max(0.0, tilt)))
    bear = max(10, int(35 + 40 * max(0.0, -tilt)))
    base = 100 - min(80, bull) - min(80, bear)
    probs = {"Bull": min(80, bull), "Base": max(10, base), "Bear": min(80, bear)}

    actions = []

    def act(title, rationale, steps, sizing, kpis, timeline, risks, mitigations, impact_score=0.7):
        actions.append({
            "title": title, "rationale": rationale, "steps": steps,
            "sizing": sizing, "kpis": kpis, "timeline": timeline,
            "risks": risks, "mitigations": mitigations, "impact_score": impact_score
        })

    act(
        "Core positioning around leading catalysts",
        f"Focus on {', '.join(top_cats[:3]) or 'dominant catalysts'} driving flows in '{query}'.",
        ["Allocate incrementally on strength with daily VWAP checks",
         "Use staggered entries at support levels from recent swing lows",
         "Review weekly vs. benchmark trend and RS (relative strength)"],
        "Starter 1–2% per position; max 6–8% theme exposure",
        ["5d RS vs. sector", "News volume delta", "30d realized vol"],
        "T+2: seed; T+7: scale on confirmation; T+30: review",
        ["Regulatory headline risk", "Crowded momentum unwind"],
        ["Tighten stops to ATR(14)*1.2", "Hedge via correlated index puts"],
        impact_score=0.85,
    )
    act(
        "Event-driven hedge",
        "Protect downside into binary events or policy windows.",
        ["Buy near-dated puts on correlated index", "Pair-trade leaders vs. laggards"],
        "Hedge 30–50% of net exposure around event windows",
        ["Skew & IV percentile", "Put-call ratio spike"],
        "T-3 to T+2 around events",
        ["IV crush post-event", "Gapping through strikes"],
        ["Use vertical spreads to reduce Vega", "Roll on large gaps"],
        impact_score=0.75,
    )
    act(
        "Data-driven monitor & rebalance",
        "Maintain discipline using objective KPIs.",
        ["Automate alerts on trigger thresholds", "Rebalance when drift > 25% from target"],
        "Monthly target rebalance ±25% drift band",
        ["Drift vs. target", "Realized/Implied ratio", "Spread breadth"],
        "Continuous; weekly check-in",
        ["Signal noise / false positives"],
        ["Use multi-signal confirmation (≥2 indicators)"],
        impact_score=0.65,
    )

    scenarios = [
        {"name": "Bull", "prob": probs["Bull"], "path": [
            "Catalyst expansion and positive surprise rate rising",
            "Breadth improves; funding and order books strengthen"
        ], "signals": ["Breakout on volume > 1.8× 20d", "EPS/guidance beats > 60% in cohort"]},
        {"name": "Base", "prob": probs["Base"], "path": [
            "Range trading with rotation across sub-themes",
            "Valuation support holds; dispersion persists"
        ], "signals": ["Realized vol within 1σ", "Macro prints close to consensus"]},
        {"name": "Bear", "prob": probs["Bear"], "path": [
            "Policy/regulatory shocks and funding stress",
            "Breadth deteriorates; leadership narrows"
        ], "signals": ["Credit/CDS widening > 15bps in peers", "Guidance cuts cluster > 3 names/wk"]},
    ]

    triggers = [
        "IF regulatory headline with 'ban'/'restriction' THEN reduce theme exposure by 30%",
        "IF price breaks 50d MA on 2× volume THEN cut weakest 30% positions",
        "IF IVP > 80 for index THEN shift to spreads / reduce long gamma",
        "IF 5d RS turns negative vs. benchmark THEN pause adds and reassess",
        "IF news volume delta > +150% day/day THEN monitor for reversal exhaustion",
    ]

    conf = score_confidence(len(historical), len(set().union(*[(h.get("catalysts") or []) for h in historical]) &
                                                set().union(*[(a.get("catalysts") or []) for a in analyzed])))

    return {
        "executive_summary": f"Nexora evaluated {len(analyzed)} developments for '{query}'. "
                             f"Key catalysts: {', '.join(top_cats) or 'broad, mixed'}. "
                             f"Average sentiment tilt {avg_sent:+.2f}.",
        "immediate_impact": "Flows favor leaders but remain headline-sensitive. Expect rotations around policy dates.",
        "scenarios": scenarios,
        "actions": actions,
        "watch_triggers": triggers,
        "confidence": conf,
    }


def strategic_reason(query: str, analyzed: List[Dict[str, Any]], historical: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Main entrypoint: LLM-first, rule-based fallback, always returns a rich brief."""
    prompt = _build_prompt(query, analyzed, historical)
    try:
        out = _REASONER(prompt, max_new_tokens=420, do_sample=False)
        text = out[0]["generated_text"]
        data = _safe_json(text)
        # Validate essential fields; if missing, fall back
        if not data or not data.get("actions") or not data.get("scenarios"):
            log.warning("Model output incomplete; using rule-based synthesis.")
            return _rule_based_brief(query, analyzed, historical)
        # Clean minimal fields
        data["executive_summary"] = clean_text(data.get("executive_summary", ""))
        data["immediate_impact"] = clean_text(data.get("immediate_impact", ""))
        if "confidence" not in data or data["confidence"] not in {"High","Medium","Low"}:
            data["confidence"] = "Medium"
        return data
    except Exception as e:
        log.error("Strategic reasoner failed: %s", e)
        return _rule_based_brief(query, analyzed, historical)
