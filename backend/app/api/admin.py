"""Admin API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from app.dependencies import require_admin_primary
from app.services.supabase import get_supabase_client
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/metrics")
async def get_admin_metrics(
    org_context: dict = Depends(require_admin_primary)
):
    """Get admin metrics (organization-level)"""
    org_id = org_context["org_id"]
    
    supabase = get_supabase_client()
    
    # Get org stats
    org_response = supabase.table("organizations") \
        .select("plan, created_at") \
        .eq("id", org_id) \
        .single() \
        .execute()
    
    if not org_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    org = org_response.data
    
    # Get briefs count (all time)
    briefs_response = supabase.table("briefs") \
        .select("id", count="exact") \
        .eq("org_id", org_id) \
        .execute()
    
    total_briefs = briefs_response.count or 0
    
    # Get briefs this month
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    briefs_month_response = supabase.table("briefs") \
        .select("id", count="exact") \
        .eq("org_id", org_id) \
        .gte("created_at", month_start.isoformat()) \
        .execute()
    
    briefs_this_month = briefs_month_response.count or 0
    
    # Get total cost
    cost_response = supabase.table("usage_events") \
        .select("cost_usd") \
        .eq("org_id", org_id) \
        .execute()
    
    total_cost = sum(float(e.get("cost_usd", 0)) for e in (cost_response.data or []))
    
    return {
        "org_id": org_id,
        "plan": org["plan"],
        "total_briefs": total_briefs,
        "briefs_this_month": briefs_this_month,
        "total_cost_usd": round(total_cost, 2),
        "created_at": org["created_at"]
    }

