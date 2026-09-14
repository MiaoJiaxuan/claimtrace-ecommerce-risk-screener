from src.llm_client import OpenRouterClient
from src.retrieval import CaseRetriever


PROVISIONAL_THRESHOLD = 0.30


class ClaimTracePipeline:
    """Run retrieval, abstention and one LLM assessment."""

    def __init__(
        self,
        threshold: float = PROVISIONAL_THRESHOLD,
    ) -> None:
        self.retriever = CaseRetriever()
        self.threshold = threshold

    def retrieve_evidence(
        self,
        claim: str,
        top_k: int = 3,
    ) -> dict:
        """Retrieve cases and check whether evidence is sufficient."""
        cases = self.retriever.retrieve(claim, top_k=top_k)

        if not cases:
            return {
                "retrieved_cases": [],
                "top_score": 0.0,
                "threshold": self.threshold,
                "evidence_sufficient": False,
                "abstain": True,
            }

        top_score = cases[0]["similarity_score"]
        evidence_sufficient = top_score >= self.threshold

        return {
            "retrieved_cases": cases,
            "top_score": top_score,
            "threshold": self.threshold,
            "evidence_sufficient": evidence_sufficient,
            "abstain": not evidence_sufficient,
        }

    def assess(
        self,
        claim: str,
        top_k: int = 3,
    ) -> dict:
        """Assess one claim and call the LLM at most once."""
        retrieval_result = self.retrieve_evidence(
            claim,
            top_k=top_k,
        )

        if retrieval_result["abstain"]:
            return {
                "llm_called": False,
                "retrieval": retrieval_result,
                "risk_card": {
                    "risk_level": "insufficient_evidence",
                    "highlighted_claim": "",
                    "reason": (
                        "The retrieved evidence is below the provisional "
                        "similarity threshold."
                    ),
                    "source_title": None,
                    "source_url": None,
                    "next_action": (
                        "Send the claim for human review before publication."
                    ),
                    "confidence": 0.0,
                    "abstain": True,
                },
                "model": None,
                "usage": {},
            }

        llm_result = OpenRouterClient().assess(
            claim,
            retrieval_result["retrieved_cases"],
        )

        return {
            "llm_called": True,
            "retrieval": retrieval_result,
            "risk_card": llm_result["risk_card"],
            "model": llm_result["model"],
            "usage": llm_result["usage"],
        }