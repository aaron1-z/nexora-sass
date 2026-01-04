"""Supabase service helpers"""
from typing import Optional, Dict, Any, List
from supabase import Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)


def get_supabase_client() -> Client:
    """Get Supabase client with service role"""
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_service_key)


async def check_usage_limit(org_id: str, event_type: str = "brief_generated") -> Dict[str, Any]:
    """Check if org has reached usage limit"""
    supabase = get_supabase_client()
    
    # Call the database function
    response = supabase.rpc("check_usage_limits", {
        "org_uuid": org_id,
        "event_type": event_type
    }).execute()
    
    if response.data:
        return response.data
    else:
        return {"allowed": True, "count": 0}


async def record_usage_event(
    org_id: str,
    user_id: str,
    event_type: str,
    metadata: Optional[Dict[str, Any]] = None,
    cost_usd: float = 0.0
) -> None:
    """Record a usage event"""
    supabase = get_supabase_client()
    
    supabase.table("usage_events").insert({
        "org_id": org_id,
        "user_id": user_id,
        "event_type": event_type,
        "metadata": metadata or {},
        "cost_usd": cost_usd
    }).execute()
    
    logger.info(f"Recorded usage event: {event_type} for org {org_id}")


async def create_audit_log(
    org_id: Optional[str],
    user_id: Optional[str],
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> None:
    """Create audit log entry"""
    supabase = get_supabase_client()
    
    supabase.table("audit_logs").insert({
        "org_id": org_id,
        "user_id": user_id,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "metadata": metadata or {},
        "ip_address": ip_address,
        "user_agent": user_agent
    }).execute()

