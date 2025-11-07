"""
Strategic reasoning with LLM + rule-based fallback
"""
from typing import List, Dict, Any
import os
import json
from statistics import mean
from collections import Counter

from .utils import log, parse_json_loose, clean_text, MODELS_DIR


# Global reasoner (lazy load)
_REASONER = None


def _load_reasoner():
    """Load flan-t5 model or return None on failure"""
    global _REASONER
    if _REASONER is not None:
        return _REASONER
    
    try:
        from transformers import pipeline
        log.info("Loading strategic reasoner (flan-t5-base)...")
        _REASONER = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1,  # CPU
            max_length=768,
            truncation=True,
            cache_dir=MODELS_DIR,
        )
        log.info("Reasoner loaded successfully")
        return _REASONER
    except Exception as e:
        log.warning(f"Failed to load reasoner model: {e}")
        return None


def _rule_based_brief(query: str, analyzed: List[Dict[str, Any]], historical: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deterministic fallback that always produces a complete brief
    """
    # Extract top catalysts and entities
    all_catalysts = []
    all_entities = []
    sentiments = []
    
    for it in analyzed:
        all_catalysts.extend(it.get("catalysts", []))
        all_entities.extend(it.get("entities", []))
        sentiments.append(it.get("sentiment", 0.0))
    
    top_catalysts = [c for c, _ in Counter(all_catalysts).most_common(6)]
    top_entities = [e for e, _ in Counter(all_entities).most_common(6)]
    avg_sent = mean(sentiments) if sentiments else 0.0
    
    # Determine scenario probabilities based on sentiment
    if avg_sent > 0.15:
        bull, base, bear = 45, 35, 20
    elif avg_sent < -0.15:
        bull, base, bear = 20, 35, 45
    else:
        bull, base, bear = 30, 40, 30
    
    # Build scenarios
    scenarios = [
        {
            "name": "Bull",
            "prob": bull,
            "path": [
                f"Positive momentum in {query} drives expansion",
                "Favorable regulatory environment emerges",
                "Key players strengthen market positions"
            ],
            "signals": [
                "Sentiment sustained above +0.3 for 5+ days",
                "Volume breakout on positive news"
            ]
        },
        {
            "name": "Base",
            "prob": base,
            "path": [
                f"Steady state in {query} with mixed signals",
                "Range-bound activity with rotational flows",
                "Wait-and-see stance from key stakeholders"
            ],
            "signals": [
                "Sentiment oscillates between -0.2 and +0.2",
                "No major catalysts trigger moves"
            ]
        },
        {
            "name": "Bear",
            "prob": bear,
            "path": [
                f"Headwinds emerge in {query}",
                "Regulatory pressures or competitive threats",
                "Market re-pricing risk premium higher"
            ],
            "signals": [
                "Sentiment breaks below -0.3",
                "Elevated mentions of risks: " + ", ".join(top_catalysts[:2])
            ]
        }
    ]
    
    # Build action plans with impact scores
    actions = []
    
    # Heuristic: higher impact if strong sentiment and many catalysts
    base_impact = 3
    if abs(avg_sent) > 0.3:
        base_impact = 4
    if len(top_catalysts) > 4:
        base_impact = min(5, base_impact + 1)
    
    actions.append({
        "title": f"Monitor {query} developments closely",
        "rationale": f"Given {len(analyzed)} recent developments and avg sentiment of {avg_sent:+.2f}, active monitoring is warranted.",
        "steps": [
            "Set up alerts for key catalysts: " + ", ".join(top_catalysts[:3]),
            "Track sentiment momentum daily",
            "Prepare scenario response playbooks"
        ],
        "sizing": "Allocate 10-20% of attention/resources",
        "kpis": [
            "Sentiment 7-day moving average",
            "Catalyst frequency (mentions/day)",
            "Source diversity index"
        ],
        "timeline": "Immediate through T+30 days",
        "risks": [
            "False signals from noise",
            "Missed inflection points",
            "Over-reaction to outliers"
        ],
        "mitigations": [
            "Use multi-signal confirmation",
            "Set appropriate thresholds",
            "Maintain balanced portfolio"
        ],
        "impact_score": base_impact
    })
    
    actions.append({
        "title": "Assess positioning relative to key entities",
        "rationale": f"Top entities identified: {', '.join(top_entities[:3] or ['various'])}. Understanding their moves informs strategy.",
        "steps": [
            "Map entity relationships and dependencies",
            "Evaluate relative strength vs peers",
            "Identify asymmetric opportunities"
        ],
        "sizing": "Focus on top 3-5 entities",
        "kpis": [
            "Entity mention share",
            "Sentiment divergence vs sector",
            "Catalyst overlap index"
        ],
        "timeline": "T+7 to T+30 days",
        "risks": [
            "Entity-specific shocks",
            "Correlation breakdown",
            "Data lag or incompleteness"
        ],
        "mitigations": [
            "Diversify across multiple entities",
            "Use real-time data where possible",
            "Maintain margin of safety"
        ],
        "impact_score": max(1, base_impact - 1)
    })
    
    # Add 2-4 more actions
    for i, catalyst in enumerate(top_catalysts[:3]):
        actions.append({
            "title": f"Prepare for {catalyst} scenarios",
            "rationale": f"'{catalyst}' is a recurring catalyst. Planning responses increases agility.",
            "steps": [
                f"Model {catalyst} impact on {query}",
                "Define trigger thresholds",
                "Pre-position resources or hedges"
            ],
            "sizing": "Proportional to catalyst frequency",
            "kpis": [
                f"{catalyst} mention velocity",
                "Response time to trigger",
                "Hedge effectiveness ratio"
            ],
            "timeline": "Ongoing through T+60",
            "risks": [
                f"{catalyst} evolves unexpectedly",
                "Timing mismatch",
                "Cost of carry on hedges"
            ],
            "mitigations": [
                "Regular catalyst review cycles",
                "Dynamic threshold adjustment",
                "Use options/asymmetric structures"
            ],
            "impact_score": 2 + (i % 2)
        })
    
    # Build watch triggers
    triggers = [
        f"IF sentiment breaks {avg_sent + 0.3:+.2f} THEN increase allocation by 20%",
        f"IF sentiment falls below {avg_sent - 0.3:+.2f} THEN reduce exposure by 30%",
        f"IF '{top_catalysts[0] if top_catalysts else 'Regulatory'}' mentions spike > 150% THEN review positioning",
        f"IF credibility-weighted sentiment diverges > 0.4 from raw THEN investigate sources",
        f"IF top entity mentions drop > 50% THEN check for structural shift",
        "IF co-occurrence of risk catalysts >= 3 in single day THEN raise alerts",
    ]
    
    # Add more IF/THEN to reach 6-12
    for catalyst in top_catalysts[1:4]:
        triggers.append(f"IF '{catalyst}' + negative sentiment >= 2 instances THEN hedge downside")
    
    # Determine confidence
    confidence = "Medium"
    if len(analyzed) >= 15 and len(historical) >= 3:
        confidence = "High"
    elif len(analyzed) < 8:
        confidence = "Low"
    
    return {
        "executive_summary": f"Analysis of {len(analyzed)} developments in '{query}' reveals avg sentiment of {avg_sent:+.2f}. Key catalysts: {', '.join(top_catalysts[:3] or ['general news'])}. Recommend active monitoring with scenario-based positioning.",
        "immediate_impact": f"Near-term outlook is {'positive' if avg_sent > 0 else 'negative' if avg_sent < 0 else 'neutral'} with moderate volatility expected. Watch for {top_catalysts[0] if top_catalysts else 'regulatory'} developments.",
        "scenarios": scenarios,
        "actions": actions,
        "watch_triggers": triggers[:12],
        "confidence": confidence,
    }


def strategic_reason(query: str, analyzed: List[Dict[str, Any]], historical: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate strategic intelligence brief
    
    Args:
        query: Focus topic
        analyzed: Recent analyzed articles
        historical: Historical context
        
    Returns:
        Complete brief dictionary matching Brief model schema
    """
    # Always try rule-based first as fallback
    fallback = _rule_based_brief(query, analyzed, historical)
    
    # Try LLM if available
    reasoner = _load_reasoner()
    if reasoner is None:
        log.info("Using rule-based brief (no LLM)")
        return fallback
    
    try:
        # Build prompt
        summary_lines = []
        for it in analyzed[:10]:
            cats = ", ".join(it.get("catalysts", [])[:3])
            summary_lines.append(f"- {it.get('title', '')[:100]} [catalysts: {cats}]")
        
        prompt = f"""You are a strategic analyst. Analyze '{query}' based on these developments:

{chr(10).join(summary_lines)}

Provide a brief with:
- Executive summary (2-3 sentences)
- Immediate impact (1-2 sentences)
- 3 scenarios: Bull/Base/Bear with probabilities summing to 100
- 4-6 action plans with impact scores 1-5
- 6-10 IF/THEN watch triggers
- Confidence: High/Medium/Low

Return ONLY valid JSON matching this schema:
{{"executive_summary": "...", "immediate_impact": "...", "scenarios": [...], "actions": [...], "watch_triggers": [...], "confidence": "Medium"}}
"""
        
        # Generate
        output = reasoner(prompt, max_new_tokens=400, do_sample=False)
        text = output[0]["generated_text"]
        
        # Parse
        data = parse_json_loose(text)
        
        # Validate essential fields
        if not data or not isinstance(data.get("scenarios"), list) or not isinstance(data.get("actions"), list):
            log.warning("LLM output invalid, using fallback")
            return fallback
        
        # Ensure impact_score exists
        for action in data.get("actions", []):
            if "impact_score" not in action:
                action["impact_score"] = 3
        
        # Merge with fallback for missing fields
        for key in fallback:
            if key not in data or not data[key]:
                data[key] = fallback[key]
        
        log.info("Generated brief using LLM")
        return data
        
    except Exception as e:
        log.error(f"LLM reasoning failed: {e}, using fallback")
        return fallback
