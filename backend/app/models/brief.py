"""Pydantic models for briefs API"""
from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class BriefGenerateRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    org_id: Optional[str] = None  # Optional - comes from auth context, not request body
    metadata: Optional[dict[str, Any]] = None


class BriefResponse(BaseModel):
    id: str
    org_id: str
    user_id: str
    title: str
    query: str
    output_data: dict[str, Any]
    confidence: Optional[str] = None
    execution_time_ms: Optional[int] = None
    cost_usd: Optional[float] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class BriefListResponse(BaseModel):
    briefs: list[BriefResponse]
    total: int
    page: int
    page_size: int

