"""Pydantic models for subscriptions"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class SubscriptionResponse(BaseModel):
    id: str
    org_id: str
    dodo_subscription_id: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    
    class Config:
        from_attributes = True


class UsageResponse(BaseModel):
    org_id: str
    plan: str
    current_period_start: Optional[datetime]
    briefs_used: int
    briefs_limit: int
    usage_percentage: float

