from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class AnalyticsEvent(BaseModel):
    event_name: str
    timestamp: datetime
    user_id: str
    properties: Dict[str, Any]

class AnalyticsService:
    def track(self, event: AnalyticsEvent):
        """
        Log event to DB or external service (PostHog/Mixpanel).
        """
        print(f"[ANALYTICS] {event.timestamp} - {event.event_name}: {event.properties}")

# Example Events
# - brief_generated
# - scenario_viewed
# - search_performed
