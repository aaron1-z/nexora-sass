from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore
from .utils import clean_text

_analyzer = SentimentIntensityAnalyzer()

def score_sentiment(text: str) -> float:
    """Return sentiment in [-1, 1]."""
    if not text:
        return 0.0
    try:
        return float(_analyzer.polarity_scores(clean_text(text))["compound"])
    except Exception:
        return 0.0
