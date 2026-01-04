"""
AI Engine Wrapper Service (CORRECTED)
"""
import time
import logging
from typing import Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

# Ensure engine is importable (path should already be set by main.py, but ensure it's there)
import sys
import os
from pathlib import Path

# Get project root (parent of backend directory)
# File is at: backend/app/services/engine.py
# So we need to go up 3 levels to get to project root
SERVICE_DIR = Path(__file__).parent  # backend/app/services
APP_DIR = SERVICE_DIR.parent          # backend/app
BACKEND_DIR = APP_DIR.parent          # backend
PROJECT_ROOT = BACKEND_DIR.parent     # project root (where engine/ is)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from engine.ingest import fetch_live_news
    from engine.reason_analyst import analyze_articles
    from engine.reason_strategic import strategic_reason
    ENGINE_AVAILABLE = True
    logger.info("✅ AI engine loaded successfully")
except Exception as e:
    ENGINE_AVAILABLE = False
    logger.error(f"❌ AI engine import failed: {e}", exc_info=True)


async def generate_brief(
    query: str,
    org_id: str,
    user_id: str,
    metadata: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Generate intelligence brief using Nexora Engine
    """
    start = time.time()

    if not ENGINE_AVAILABLE:
        return _failed("AI engine not available", start)

    try:
        # -------------------------------
        # 1️⃣ Fetch news (ASYNC)
        # -------------------------------
        logger.info(f"📰 Fetching news for: {query}")
        articles = await fetch_live_news(
            query=query,
            limit=20,
            expand=True,
        )

        if not articles:
            return _failed("No news articles found", start)

        # -------------------------------
        # 2️⃣ Analyze (SYNC)
        # -------------------------------
        logger.info(f"🔬 Analyzing {len(articles)} articles")
        analyzed = analyze_articles(articles)

        # -------------------------------
        # 3️⃣ Strategic reasoning (SYNC)
        # -------------------------------
        logger.info("🧠 Generating strategic brief")
        brief = strategic_reason(query, analyzed, historical=[])

        exec_ms = int((time.time() - start) * 1000)

        return {
            "status": "completed",
            "output_data": brief,
            "input_data": {
                "query": query,
                "articles_count": len(articles),
                "analyzed_count": len(analyzed),
            },
            "execution_time_ms": exec_ms,
            "cost_usd": 0.01,
            "confidence": brief.get("confidence", "Medium"),
            "error_message": None,
        }

    except Exception as e:
        logger.error("❌ Brief generation failed", exc_info=True)
        return _failed(str(e), start)


def _failed(msg: str, start: float) -> Dict[str, Any]:
    return {
        "status": "failed",
        "output_data": {},
        "input_data": {},
        "execution_time_ms": int((time.time() - start) * 1000),
        "cost_usd": 0.0,
        "confidence": None,
        "error_message": msg,
    }
