from typing import List
import re

_CATALYSTS = {
    "M&A": [r"\bmerger\b", r"\bacquisition\b", r"\btakeover\b"],
    "Earnings": [r"\bearnings\b", r"\bEPS\b", r"\bresults?\b", r"\bguidance\b"],
    "Regulatory": [r"\bregulator|regulatory|ban|approve|lawsuit|antitrust|sanction(s)?\b"],
    "Macroeconomy": [r"\binflation\b", r"\brate hike\b", r"\bCPI\b", r"\bGDP\b"],
    "Product/Tech": [r"\blaunch\b", r"\brelease\b", r"\bAI\b", r"\bchip(s)?\b", r"\bR&D\b"],
    "Geopolitics": [r"\btariff(s)?\b", r"\bconflict\b", r"\bwar\b", r"\bexport control(s)?\b"],
    "ESG": [r"\bclimate\b", r"\bemission(s)?\b", r"\bESG\b", r"\bsustainab"],
    "Supply Chain": [r"\bshortage\b", r"\bsupply chain\b", r"\blogistics\b", r"\bbacklog\b"],
}

def classify_catalysts(text: str) -> List[str]:
    if not text: return []
    t = text.lower()
    labels = []
    for lab, pats in _CATALYSTS.items():
        if any(re.search(p, t) for p in pats):
            labels.append(lab)
    return list(dict.fromkeys(labels))[:6]
