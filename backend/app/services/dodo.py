"""
Dodo Payments integration service
Handles:
- Checkout creation
- Webhook processing
- Credit granting
- Credit availability checks
"""
import logging
from typing import Dict, Any, Optional
import requests
import json

from app.config import settings
from app.services.supabase import get_supabase_client

logger = logging.getLogger(__name__)


# ==================================================
# Create Checkout Session
# ==================================================

def create_checkout_session(
    org_id: str,
    success_url: str,
    cancel_url: str,
) -> Dict[str, Any]:
    """
    Creates a Dodo checkout session using production API.
    """
    
    # --------------------------------------------------
    # 🚀 PRODUCTION MODE (REAL DODO)
    # --------------------------------------------------
    if not settings.dodo_api_key or not settings.dodo_product_brief:
        raise RuntimeError("Dodo is not configured correctly. Please set DODO_API_KEY and DODO_PRODUCT_BRIEF")

    payload = {
        "product_cart": [
            {
                "product_id": settings.dodo_product_brief,
                "quantity": 1,
            }
        ],
        "redirect_urls": {
            "success": success_url,
            "cancel": cancel_url,
        },
        "metadata": {
            "org_id": org_id,
            "type": "brief_purchase",
        },
    }

    headers = {
        "Authorization": f"Bearer {settings.dodo_api_key}",
        "Content-Type": "application/json",
    }

    try:
        # Dodo Payments API endpoint
        # Correct URL format: https://api.dodopayments.com/checkout_sessions
        base_url = settings.dodo_api_url.rstrip('/')
        
        # Auto-correct common mistakes
        if 'api.dodo.com' in base_url and 'dodopayments' not in base_url:
            logger.warning(f"⚠️  Auto-correcting incorrect API URL: {base_url}")
            base_url = base_url.replace('api.dodo.com', 'api.dodopayments.com')
            logger.info(f"✅ Using corrected URL: {base_url}")
        
        # Validate URL is correct
        if 'dodopayments' not in base_url.lower():
            logger.error(f"❌ INCORRECT API URL: {base_url}")
            logger.error(f"⚠️  Should be: https://api.dodopayments.com")
            raise RuntimeError(
                f"Incorrect Dodo API URL: {base_url}. "
                f"Please set DODO_API_URL=https://api.dodopayments.com in your backend/.env.local file"
            )
        
        api_endpoint = f"{base_url}/checkout_sessions"
        
        logger.info(f"Creating Dodo checkout session at: {api_endpoint}")
        logger.info(f"Payload: {json.dumps({**payload, 'metadata': payload.get('metadata', {})}, indent=2)}")
        
        response = requests.post(
            api_endpoint,
            headers=headers,
            json=payload,
            timeout=30,
        )
        
        logger.info(f"Dodo API response status: {response.status_code}")
        logger.info(f"Dodo API response: {response.text[:500]}")
        
    except requests.exceptions.ConnectionError as e:
        error_msg = str(e)
        logger.error(f"Dodo connection failed: {error_msg}", exc_info=True)
        raise RuntimeError(f"Failed to connect to Dodo Payments API. Please check your internet connection and DODO_API_URL setting. Error: {error_msg}")
    except requests.RequestException as e:
        logger.error(f"Dodo API request failed: {e}", exc_info=True)
        raise RuntimeError(f"Payment provider unavailable: {str(e)}")

    if not response.ok:
        error_detail = response.text
        try:
            error_json = response.json()
            error_detail = error_json.get("message") or error_json.get("error") or error_detail
        except:
            pass
        logger.error(f"Dodo checkout failed ({response.status_code}): {error_detail}")
        raise RuntimeError(f"Failed to create checkout session: {error_detail}")

    try:
        session = response.json()
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON response from Dodo: {response.text}")
        raise RuntimeError("Invalid response from payment provider")

    session_id = session.get("id") or session.get("session_id")
    checkout_url = (
        session.get("checkout_url") 
        or session.get("url") 
        or session.get("redirect_url")
        or session.get("checkout_urls", {}).get("success")
    )

    if not session_id or not checkout_url:
        logger.error(f"Incomplete checkout session response: {session}")
        raise RuntimeError("Incomplete response from payment provider")

    logger.info(f"✅ Dodo checkout created: {session_id}")

    return {
        "id": session_id,
        "checkout_url": checkout_url,
        "session_id": session_id,
    }


# ==================================================
# Webhook Handler
# ==================================================

def handle_webhook_event(event: Dict[str, Any]) -> None:
    """
    Processes Dodo webhook events.
    Grants credit ONLY on confirmed payment success.
    """

    event_type = event.get("type") or event.get("event_type")
    data = event.get("data") or event.get("object") or {}

    SUCCESS_EVENTS = {
        "checkout.session.completed",
        "checkout.session.complete",
        "payment.completed",
        "payment.success",
        "payment.succeeded",
        "charge.succeeded",
    }

    logger.info(f"Processing webhook event: {event_type}")

    if event_type not in SUCCESS_EVENTS:
        logger.info(f"Ignoring webhook event: {event_type}")
        return

    # Try multiple possible metadata locations
    metadata = (
        data.get("metadata") 
        or data.get("custom_metadata")
        or event.get("metadata")
        or {}
    )
    
    # org_id might be in metadata or in the checkout session
    org_id = metadata.get("org_id")
    
    # If not in metadata, try to get from checkout session
    if not org_id and "checkout_session" in data:
        checkout_meta = data.get("checkout_session", {}).get("metadata", {})
        org_id = checkout_meta.get("org_id")
    
    # If still not found, try session metadata
    if not org_id and "session" in data:
        session_meta = data.get("session", {}).get("metadata", {})
        org_id = session_meta.get("org_id")

    if not org_id:
        logger.warning(f"Webhook missing org_id in event: {json.dumps(event, default=str)[:500]}")
        return

    # Payment/session IDs - try multiple possible fields
    payment_id = (
        data.get("id")
        or data.get("payment_id")
        or data.get("charge_id")
        or data.get("checkout_session", {}).get("id")
        or data.get("session", {}).get("id")
    )
    
    session_id = (
        data.get("session_id")
        or data.get("checkout_session_id")
        or data.get("checkout_session", {}).get("id")
        or data.get("session", {}).get("id")
    )

    if not payment_id and not session_id:
        logger.warning(f"Webhook missing payment_id and session_id: {json.dumps(event, default=str)[:500]}")
        return

    # Use session_id as payment_id if payment_id not available
    if not payment_id:
        payment_id = session_id

    logger.info(f"Processing payment for org {org_id}, payment_id: {payment_id}")

    _grant_credit(
        org_id=org_id,
        payment_id=payment_id,
        session_id=session_id,
        amount=settings.brief_price_usd,
        mock=False,
    )


# ==================================================
# Credit Grant (IDEMPOTENT)
# ==================================================

def _grant_credit(
    org_id: str,
    payment_id: str,
    session_id: Optional[str],
    amount: float,
    mock: bool = False,
) -> None:
    """
    Grants one brief credit.
    Fully idempotent (safe against double webhooks).
    """

    supabase = get_supabase_client()

    # 🔒 Idempotency guard - check if this payment_id already exists
    try:
        # Query for existing payment with this payment_id in metadata
        existing = (
            supabase.table("usage_events")
            .select("id, metadata")
            .eq("event_type", "brief_payment_completed")
            .eq("org_id", org_id)
            .execute()
        )
        
        # Check metadata for matching payment_id
        if existing.data:
            for event in existing.data:
                meta = event.get("metadata") or {}
                if isinstance(meta, str):
                    try:
                        meta = json.loads(meta)
                    except:
                        meta = {}
                
                if meta.get("payment_id") == payment_id:
                    logger.info(f"Payment {payment_id} already recorded for org {org_id}, skipping credit grant")
                    return
    except Exception as e:
        logger.warning(f"Idempotency check failed, proceeding anyway: {e}")

    supabase.table("usage_events").insert({
        "org_id": org_id,
        "event_type": "brief_payment_completed",
        "metadata": {
            "payment_id": payment_id,
            "session_id": session_id,
            "amount": amount,
            "mock": mock,
        },
        "cost_usd": amount,
    }).execute()

    logger.info(f"✅ Credit granted to org {org_id} (mock={mock})")


# ==================================================
# Credit Availability Check
# ==================================================

def check_payment_credit(org_id: str) -> Dict[str, Any]:
    """
    Determines whether an org has unused paid credits.
    """

    supabase = get_supabase_client()

    payments = (
        supabase.table("usage_events")
        .select("id", count="exact")
        .eq("org_id", org_id)
        .eq("event_type", "brief_payment_completed")
        .execute()
    )

    briefs = (
        supabase.table("briefs")
        .select("id", count="exact")
        .eq("org_id", org_id)
        .execute()
    )

    total_paid = payments.count or 0
    total_used = briefs.count or 0
    available = max(0, total_paid - total_used)

    return {
        "has_credit": available > 0,
        "available_credits": available,
        "total_paid": total_paid,
        "total_used": total_used,
    }

