from .utils import domain_of

# Simple domain credibility weights (0..1). Extend as needed.
_DOMAIN_WEIGHTS = {
    "reuters.com": 0.95,
    "bloomberg.com": 0.95,
    "apnews.com": 0.9,
    "wsj.com": 0.9,
    "ft.com": 0.9,
    "techcrunch.com": 0.75,
    "theverge.com": 0.7,
}

def score_credibility(url: str) -> float:
    host = domain_of(url)
    return _DOMAIN_WEIGHTS.get(host, 0.6)  # default neutral credibility
