"""
Dodo Payments API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.dependencies import require_analyst_or_admin_primary
from app.services.dodo import create_checkout_session, handle_webhook_event
from app.config import settings
import logging
import hmac
import hashlib
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dodo", tags=["dodo"])


# ==================================================
# Create Checkout
# ==================================================

@router.post("/create-checkout")
async def create_checkout(
    org_context: dict = Depends(require_analyst_or_admin_primary),
):
    org_id = org_context["org_id"]

    # 🔒 Hard guard
    if not settings.dodo_product_brief:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dodo product ID not configured",
        )

    # Resolve frontend safely
    frontend = (
        settings.cors_origins_list[0]
        if settings.cors_origins_list
        else "http://localhost:3000"
    )

    success_url = f"{frontend}/briefs?payment=success"
    cancel_url = f"{frontend}/briefs?payment=cancel"

    try:
        session = create_checkout_session(
            org_id=org_id,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        checkout_url = (
            session.get("checkout_url")
            or session.get("url")
            or session.get("redirect_url")
        )

        if not checkout_url:
            logger.error(f"Invalid checkout session response: {session}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Checkout URL missing from payment provider",
            )

        session_id = session.get("id") or session.get("session_id")
        
        logger.info(f"✅ Checkout created for org {org_id}, session: {session_id}")

        return {
            "checkout_url": checkout_url,
            "session_id": session_id,
            "mock": session.get("mock", False),
        }

    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"Checkout creation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error("Checkout creation failed", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create checkout session: {str(e)}",
        )


# ==================================================
# Webhook (CRITICAL PATH)
# ==================================================

@router.post("/webhook")
async def dodo_webhook(request: Request):
    payload = await request.body()

    signature = (
        request.headers.get("x-dodo-signature")
        or request.headers.get("signature")
        or request.headers.get("x-signature")
    )

    # --------------------------------------------------
    # 🔐 Signature verification
    # --------------------------------------------------
    if settings.dodo_webhook_secret:
        if not signature:
            logger.warning("Webhook missing signature header")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing signature header",
            )
        
        # Dodo Payments typically sends signature as timestamp,signature or just signature
        # Handle both formats
        if "," in signature:
            # Format: timestamp,signature
            timestamp, sig = signature.split(",", 1)
        else:
            sig = signature
        
        # Compute expected signature
        # Dodo uses HMAC-SHA256 with the webhook secret
        expected = hmac.new(
            settings.dodo_webhook_secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        # Compare signatures (support both hex and base64 potentially)
        if not (hmac.compare_digest(sig, expected) or hmac.compare_digest(signature, expected)):
            logger.warning(f"Invalid Dodo webhook signature. Expected: {expected[:20]}..., Got: {sig[:20] if sig else 'None'}...")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature",
            )
        
        logger.info("✅ Webhook signature verified")

    # --------------------------------------------------
    # Parse payload
    # --------------------------------------------------
    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload",
        )

    # --------------------------------------------------
    # Process webhook
    # --------------------------------------------------
    try:
        handle_webhook_event(event)
    except Exception as e:
        logger.error("Webhook processing failed", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed",
        )

    return {"status": "ok"}

