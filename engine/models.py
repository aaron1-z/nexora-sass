"""
Pydantic models for Nexora Intelligence Workbench
"""
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class Headline(BaseModel):
    id: str
    title: str
    summary: str = ""
    source: str = "News"
    link: str = ""
    timestamp: float
    sentiment: float = 0.0
    credibility: float = 0.9
    catalysts: List[str] = []
    entities: List[str] = []


class Scenario(BaseModel):
    name: str
    prob: int = Field(ge=0, le=100)
    path: List[str] = []
    signals: List[str] = []


class ActionPlan(BaseModel):
    title: str
    rationale: str = ""
    steps: List[str] = []
    sizing: str = ""
    kpis: List[str] = []
    timeline: str = ""
    risks: List[str] = []
    mitigations: List[str] = []
    impact_score: int = Field(default=3, ge=1, le=5)


class Brief(BaseModel):
    executive_summary: str = ""
    immediate_impact: str = ""
    scenarios: List[Scenario] = []
    actions: List[ActionPlan] = []
    watch_triggers: List[str] = []
    confidence: str = "Medium"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
