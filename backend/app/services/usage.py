"""Usage tracking service"""
from typing import Dict, Any
from datetime import datetime, timedelta
from app.services.supabase import get_supabase_client
import logging

logger = logging.getLogger(__name__)


async def get_usage_stats(org_id: str) -> Dict[str, Any]:
    """Get usage statistics for an org"""
    supabase = get_supabase_client()
    
    # Get org info
    org_response = supabase.table("organizations") \
        .select("plan, created_at") \
        .eq("id", org_id) \
        .single() \
        .execute()
    
    if not org_response.data:
        raise ValueError(f"Organization {org_id} not found")
    
    org = org_response.data
    plan = org["plan"]
    
    # Get current period (monthly billing cycle)
    # For simplicity, use calendar month
    now = datetime.utcnow()
    period_start = datetime(now.year, now.month, 1)
    
    # Get subscription period if exists
    sub_response = supabase.table("subscriptions") \
        .select("current_period_start") \
        .eq("org_id", org_id) \
        .eq("status", "active") \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()
    
    if sub_response.data:
        period_start = datetime.fromisoformat(
            sub_response.data[0]["current_period_start"].replace("Z", "+00:00")
        ).replace(tzinfo=None)
    
    # Count briefs this period
    briefs_response = supabase.table("usage_events") \
        .select("id", count="exact") \
        .eq("org_id", org_id) \
        .eq("event_type", "brief_generated") \
        .gte("created_at", period_start.isoformat()) \
        .execute()
    
    briefs_used = briefs_response.count or 0
    
    # Get limits based on plan
    limits = {
        "starter": 10,
        "pro": 100,
        "enterprise": 999999
    }
    
    briefs_limit = limits.get(plan, 10)
    usage_percentage = (briefs_used / briefs_limit * 100) if briefs_limit > 0 else 0
    
    return {
        "org_id": org_id,
        "plan": plan,
        "current_period_start": period_start.isoformat(),
        "briefs_used": briefs_used,
        "briefs_limit": briefs_limit,
        "usage_percentage": round(usage_percentage, 2)
    }

