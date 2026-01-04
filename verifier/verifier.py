from typing import Dict, List

class Verifier:
    def __init__(self):
        pass

    def verify_claim(self, claim: str, evidence: List[str]) -> Dict:
        """
        Verify a claim against evidence using NLI or self-consistency.
        """
        # Mock logic: check if keywords from claim exist in evidence
        score = 0.0
        for ev in evidence:
            if any(word in ev for word in claim.split()):
                score += 0.5
        
        confidence = min(score, 1.0)
        return {
            "claim": claim,
            "supported": confidence > 0.7,
            "confidence": confidence,
            "supporting_evidence": evidence[:1] if confidence > 0 else []
        }

if __name__ == "__main__":
    v = Verifier()
    print(v.verify_claim("Market is up", ["The market rose by 2% today."]))
