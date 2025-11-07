"""
Nexora Intelligence Engine - YC-Ready Edition
Core modules for intelligence gathering and analysis
"""

# Models
from .models import Headline, Scenario, ActionPlan, Brief

# Utils
from .utils import (
    ensure_dirs,
    clean_text,
    time_ago,
    highlight,
    save_zip_bundle,
    dedupe_by_id,
    hash_string,
    parse_json_loose,
    safe_export_json,
    read_jsonl,
    append_jsonl,
    get_cached,
    set_cached,
    clear_cache,
    log,
    DATA_DIR,
    MODELS_DIR,
    CACHE_DIR,
)

# Ingest
from .ingest import fetch_live_news, expand_terms

# Reasoning
from .reason_strategic import strategic_reason

# Trends
from .trends import build_trends, momentum_report

# Research
from .research import cluster_topics, source_heatmap

# Alerts
from .alerts import load_rules, save_rules, run_rules, backtest_rule

# Tasks
from .tasks import TaskLoop

__all__ = [
    # Models
    "Headline",
    "Scenario",
    "ActionPlan",
    "Brief",
    # Utils
    "ensure_dirs",
    "clean_text",
    "time_ago",
    "highlight",
    "save_zip_bundle",
    "dedupe_by_id",
    "hash_string",
    "parse_json_loose",
    "safe_export_json",
    "read_jsonl",
    "append_jsonl",
    "get_cached",
    "set_cached",
    "clear_cache",
    "log",
    "DATA_DIR",
    "MODELS_DIR",
    "CACHE_DIR",
    # Ingest
    "fetch_live_news",
    "expand_terms",
    # Reasoning
    "strategic_reason",
    # Trends
    "build_trends",
    "momentum_report",
    # Research
    "cluster_topics",
    "source_heatmap",
    # Alerts
    "load_rules",
    "save_rules",
    "run_rules",
    "backtest_rule",
    # Tasks
    "TaskLoop",
]
