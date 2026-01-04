from typing import Dict, List
from datetime import datetime

class ActionBriefGenerator:
    def __init__(self):
        pass

    def generate_brief(self, topic: str, insights: List[str], recommendations: List[str]) -> Dict:
        """
        Generate a structured JSON action brief.
        """
        return {
            "brief_id": f"brief_{int(datetime.now().timestamp())}",
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": " ".join(insights[:2]),
            "key_insights": insights,
            "strategic_recommendations": recommendations,
            "priority": "HIGH" if "urgent" in topic.lower() else "MEDIUM"
        }

if __name__ == "__main__":
    gen = ActionBriefGenerator()
    print(gen.generate_brief("Competitor Analysis", ["Competitor X launched product Y"], ["Monitor pricing"]))
