"""Usage API endpoints - simplified for pay-per-brief model"""
from fastapi import APIRouter, Depends
from app.models.subscription import UsageResponse
from app.dependencies import require_analyst_or_admin_primary
from app.services.dodo import check_payment_credit
from app.config import settings
from datetime import datetime

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("", response_model=UsageResponse)
async def get_usage(
    org_context: dict = Depends(require_analyst_or_admin_primary)
):
    """Get usage statistics for an organization - uses primary org from auth context"""
    org_id = org_context["org_id"]
    
    
    credit_check = check_payment_credit(org_id)
    
    # For pay-per-brief model, return credit information
    return UsageResponse(
        org_id=org_id,
        plan="pay-per-brief",
        current_period_start=None,
        briefs_used=credit_check["total_used"],
        briefs_limit=credit_check["total_paid"],  # Limit is based on payments
        usage_percentage=100.0 if credit_check["total_paid"] == 0 else (credit_check["total_used"] / credit_check["total_paid"] * 100)
    )
