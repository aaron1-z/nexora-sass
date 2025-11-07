"""
Alert rules DSL with backtesting
"""
from typing import List, Dict, Any
import json
import os

from .utils import log, DATA_DIR


RULES_PATH = os.path.join(DATA_DIR, "rules.json")


def load_rules() -> List[Dict[str, Any]]:
    """Load alert rules from disk"""
    if not os.path.exists(RULES_PATH):
        return []
    
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            rules = json.load(f)
        log.info(f"Loaded {len(rules)} rules")
        return rules
    except Exception as e:
        log.error(f"Failed to load rules: {e}")
        return []


def save_rules(rules: List[Dict[str, Any]]) -> None:
    """Save alert rules to disk"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(RULES_PATH, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2)
        log.info(f"Saved {len(rules)} rules")
    except Exception as e:
        log.error(f"Failed to save rules: {e}")


def _match_rule(rule: Dict[str, Any], row: Dict[str, Any]) -> bool:
    """
    Check if a headline matches a rule
    
    Rule format:
        {
            "name": "...",
            "any": ["keyword:X", "catalyst:Y"],  # OR conditions
            "all": ["sentiment>=0.2"],  # AND conditions
            "min_sentiment": 0.2,
            "min_credibility": 0.6,
            ...
        }
    """
    # Check ANY conditions (at least one must match)
    any_conditions = rule.get("any", [])
    if any_conditions:
        any_match = False
        for cond in any_conditions:
            if ":" in cond:
                typ, val = cond.split(":", 1)
                typ = typ.strip().lower()
                val = val.strip().lower()
                
                if typ == "keyword" and val in row.get("title", "").lower():
                    any_match = True
                    break
                elif typ == "catalyst" and any(val in c.lower() for c in row.get("catalysts", [])):
                    any_match = True
                    break
                elif typ == "entity" and any(val in e.lower() for e in row.get("entities", [])):
                    any_match = True
                    break
                elif typ == "source" and val in row.get("source", "").lower():
                    any_match = True
                    break
        
        if not any_match:
            return False
    
    # Check ALL conditions (all must match)
    all_conditions = rule.get("all", [])
    for cond in all_conditions:
        if ">=" in cond:
            field, val = cond.split(">=")
            field = field.strip()
            threshold = float(val.strip())
            if field == "sentiment" and row.get("sentiment", 0.0) < threshold:
                return False
            elif field == "credibility" and row.get("credibility", 0.0) < threshold:
                return False
        elif "<=" in cond:
            field, val = cond.split("<=")
            field = field.strip()
            threshold = float(val.strip())
            if field == "sentiment" and row.get("sentiment", 0.0) > threshold:
                return False
            elif field == "credibility" and row.get("credibility", 0.0) > threshold:
                return False
    
    # Check min thresholds
    if "min_sentiment" in rule and row.get("sentiment", 0.0) < rule["min_sentiment"]:
        return False
    if "min_credibility" in rule and row.get("credibility", 0.0) < rule["min_credibility"]:
        return False
    
    return True


def run_rules(rules: List[Dict[str, Any]], flash: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run all rules against flash data and return alerts
    
    Returns:
        List of alert dicts with: title, source, link, sentiment, severity, rule_name
    """
    alerts = []
    
    for rule in rules:
        if not rule.get("enabled", True):
            continue
        
        for row in flash:
            if _match_rule(rule, row):
                alerts.append({
                    "title": row.get("title", ""),
                    "source": row.get("source", ""),
                    "link": row.get("link", ""),
                    "sentiment": row.get("sentiment", 0.0),
                    "severity": rule.get("severity", "Medium"),
                    "rule_name": rule.get("name", "Unnamed"),
                    "timestamp": row.get("timestamp", 0),
                })
    
    # Sort by severity (High > Medium > Low)
    severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    alerts.sort(key=lambda x: severity_order.get(x["severity"], 0), reverse=True)
    
    return alerts


def backtest_rule(rule: Dict[str, Any], history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Backtest a rule over historical data
    
    Returns:
        Dict with: matches, precision_proxy, avg_sentiment
    """
    matches = []
    
    for row in history:
        if _match_rule(rule, row):
            matches.append(row)
    
    if not matches:
        return {
            "matches": 0,
            "precision_proxy": 0.0,
            "avg_sentiment": 0.0,
            "sample_matches": [],
        }
    
    # Calculate metrics
    sentiments = [m.get("sentiment", 0.0) for m in matches]
    avg_sent = sum(sentiments) / len(sentiments)
    
    # Precision proxy: how many matches had |sentiment| >= 0.6 (significant)
    significant = sum(1 for s in sentiments if abs(s) >= 0.6)
    precision = significant / len(matches) if matches else 0.0
    
    return {
        "matches": len(matches),
        "precision_proxy": round(precision, 2),
        "avg_sentiment": round(avg_sent, 3),
        "sample_matches": matches[:5],
    }
