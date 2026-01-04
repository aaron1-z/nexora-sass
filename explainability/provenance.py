from typing import Dict, List

class ExplainabilityLayer:
    def __init__(self):
        pass

    def generate_provenance_map(self, reasoning_trace: Dict) -> Dict:
        """
        Map each step of reasoning to its source evidence.
        """
        steps = reasoning_trace.get("steps", [])
        provenance = []
        for step in steps:
            provenance.append({
                "step_id": step.get("step"),
                "claim": step.get("thought"),
                "sources": [step.get("evidence")] # In real app, this would be IDs/URLs
            })
        return {"provenance_chain": provenance}

    def format_chain_of_thought(self, trace: Dict) -> str:
        """
        Convert internal trace to human-readable explanation.
        """
        output = "Reasoning Process:\n"
        for step in trace.get("steps", []):
            output += f"{step['step']}. {step['thought']} (Source: {step['evidence']})\n"
        output += f"\nConclusion: {trace.get('conclusion')}"
        return output

if __name__ == "__main__":
    exp = ExplainabilityLayer()
    mock_trace = {
        "steps": [{"step": 1, "thought": "A implies B", "evidence": "Doc 1"}],
        "conclusion": "B is true"
    }
    print(exp.format_chain_of_thought(mock_trace))
