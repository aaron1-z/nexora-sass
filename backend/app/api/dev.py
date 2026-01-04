"""Development/Testing endpoints - ONLY for local development"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import require_analyst_or_admin_primary
from app.services.supabase import get_supabase_client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dev", tags=["dev"])


@router.post("/grant-credit")
async def grant_payment_credit(
    org_context: dict = Depends(require_analyst_or_admin_primary)
):
    """
    DEV ONLY: Grant a payment credit for testing without real payment.
    This simulates a successful payment.
    DO NOT USE IN PRODUCTION!
    """
    # Only allow in development mode
    if settings.environment == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in development mode"
        )
    
    org_id = org_context["org_id"]
    supabase = get_supabase_client()
    
    # Create a fake payment event to grant credit
    supabase.table("usage_events").insert({
        "org_id": org_id,
        "event_type": "brief_payment_completed",
        "metadata": {
            "payment_id": f"test_payment_{org_id}",
            "session_id": f"test_session_{org_id}",
            "amount": settings.brief_price_usd,
            "grants_brief": True,
            "test_mode": True
        },
        "cost_usd": settings.brief_price_usd
    }).execute()
    
    logger.info(f"Granted test credit to org {org_id}")
    
    return {
        "success": True,
        "message": "Payment credit granted (test mode)",
        "org_id": org_id,
        "credit_amount": 1
    }


@router.post("/clear-credits")
async def clear_credits(
    org_context: dict = Depends(require_analyst_or_admin_primary)
):
    """
    DEV ONLY: Clear all payment credits for testing.
    DO NOT USE IN PRODUCTION!
    """
    if settings.environment == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in development mode"
        )
    
    org_id = org_context["org_id"]
    supabase = get_supabase_client()
    
    # Delete test payment events
    supabase.table("usage_events") \
        .delete() \
        .eq("org_id", org_id) \
        .eq("event_type", "brief_payment_completed") \
        .eq("metadata->test_mode", "true") \
        .execute()
    
    logger.info(f"Cleared test credits for org {org_id}")
    
    return {
        "success": True,
        "message": "Test credits cleared"
    }

