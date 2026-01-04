"""Briefs API endpoints (NON-BLOCKING, SAFE)"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.models.brief import (
    BriefGenerateRequest,
    BriefResponse,
    BriefListResponse,
)
from app.dependencies import (
    require_analyst_or_admin_primary,
    get_current_user,
)
from app.services.engine import generate_brief
from app.services.supabase import (
    get_supabase_client,
    record_usage_event,
    create_audit_log,
)
from app.services.dodo import check_payment_credit
from app.config import settings
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/briefs", tags=["briefs"])


# ---------------------------------------------------------
# Background worker
# ---------------------------------------------------------

async def _run_brief_generation(
    brief_id: str,
    query: str,
    org_id: str,
    user_id: str,
    metadata: dict | None,
):
    supabase = get_supabase_client()
    start = time.time()

    try:
        result = await generate_brief(
            query=query,
            org_id=org_id,
            user_id=user_id,
            metadata=metadata,
        )

        update = {
            "output_data": result.get("output_data", {}),
            "input_data": result.get("input_data", {}),
            "confidence": result.get("confidence"),
            "execution_time_ms": result.get("execution_time_ms"),
            "cost_usd": result.get("cost_usd", 0.0),
            "status": result.get("status", "completed"),
            "error_message": result.get("error_message"),
        }

        supabase.table("briefs").update(update).eq("id", brief_id).execute()

        # Consume credit
        await record_usage_event(
            org_id=org_id,
            user_id=user_id,
            event_type="brief_generated",
            metadata={"brief_id": brief_id},
            cost_usd=settings.brief_price_usd,
        )

        await create_audit_log(
            org_id=org_id,
            user_id=user_id,
            action="brief_generated",
            resource_type="brief",
            resource_id=brief_id,
        )

        elapsed = int((time.time() - start) * 1000)
        logger.info(f"Brief {brief_id} completed in {elapsed}ms")

    except Exception as e:
        logger.error(f"Background brief failed: {e}", exc_info=True)
        supabase.table("briefs").update({
            "status": "failed",
            "error_message": str(e),
        }).eq("id", brief_id).execute()


# ---------------------------------------------------------
# Generate Brief (NON-BLOCKING)
# ---------------------------------------------------------

@router.post(
    "/generate",
    response_model=BriefResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_brief_endpoint(
    request: BriefGenerateRequest,
    background_tasks: BackgroundTasks,
    org_context: dict = Depends(require_analyst_or_admin_primary),
    user_info: dict = Depends(get_current_user),
):
    org_id = org_context["org_id"]
    user_id = user_info["user_id"]

    # 1️⃣ Check credit
    credit = check_payment_credit(org_id)
    if not credit["has_credit"]:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "message": "Payment required to generate brief",
                "price": settings.brief_price_usd,
                "available_credits": credit["available_credits"],
            },
        )

    supabase = get_supabase_client()

    # 2️⃣ Create PENDING brief
    payload = {
        "org_id": org_id,
        "user_id": user_id,
        "title": request.query[:100],
        "query": request.query,
        "status": "processing",
        "confidence": None,
        "input_data": {},
        "output_data": {},
        "execution_time_ms": None,
        "cost_usd": None,
    }

    insert = supabase.table("briefs").insert(payload).execute()
    if not insert.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create brief",
        )

    brief = insert.data[0]

    # 3️⃣ Run generation in background
    background_tasks.add_task(
        _run_brief_generation,
        brief["id"],
        request.query,
        org_id,
        user_id,
        request.metadata,
    )

    logger.info(f"Brief {brief['id']} queued for generation")

    return BriefResponse(**brief)


# ---------------------------------------------------------
# Payment / Credit Status
# ---------------------------------------------------------

@router.get("/payment-status")
async def get_payment_status(
    org_context: dict = Depends(require_analyst_or_admin_primary),
):
    org_id = org_context["org_id"]
    credit = check_payment_credit(org_id)

    return {
        "has_credit": credit["has_credit"],
        "available_credits": credit["available_credits"],
        "price_per_brief": settings.brief_price_usd,
        "total_paid": credit["total_paid"],
        "total_used": credit["total_used"],
    }


# ---------------------------------------------------------
# List Briefs
# ---------------------------------------------------------

@router.get("", response_model=BriefListResponse)
async def list_briefs(
    page: int = 1,
    page_size: int = 20,
    org_context: dict = Depends(require_analyst_or_admin_primary),
):
    org_id = org_context["org_id"]
    supabase = get_supabase_client()

    count = (
        supabase.table("briefs")
        .select("id", count="exact")
        .eq("org_id", org_id)
        .execute()
    ).count or 0

    offset = (page - 1) * page_size
    data = (
        supabase.table("briefs")
        .select("*")
        .eq("org_id", org_id)
        .order("created_at", desc=True)
        .range(offset, offset + page_size - 1)
        .execute()
    ).data or []

    briefs = [BriefResponse(**b) for b in data]

    return BriefListResponse(
        briefs=briefs,
        total=count,
        page=page,
        page_size=page_size,
    )


# ---------------------------------------------------------
# Get Single Brief
# ---------------------------------------------------------

@router.get("/{brief_id}", response_model=BriefResponse)
async def get_brief(
    brief_id: str,
    org_context: dict = Depends(require_analyst_or_admin_primary),
):
    org_id = org_context["org_id"]
    supabase = get_supabase_client()

    resp = (
        supabase.table("briefs")
        .select("*")
        .eq("id", brief_id)
        .eq("org_id", org_id)
        .single()
        .execute()
    )

    if not resp.data:
        raise HTTPException(status_code=404, detail="Brief not found")

    return BriefResponse(**resp.data)
