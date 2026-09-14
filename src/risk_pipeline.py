from src.retrieval import CaseRetriever


PROVISIONAL_THRESHOLD = 0.30


class ClaimTracePipeline:
    """Run the retrieval stage of the ClaimTrace prototype."""

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
        """Retrieve cases and decide whether the evidence is sufficient."""
        cases = self.retriever.retrieve(claim, top_k=top_k)

        if not cases:
            return {
                "retrieved_cases": [],
                "top_score": 0.0,
                "threshold": self.threshold,
                "evidence_sufficient": False,
                "abstain": True,
                "message": (
                    "No evidence was retrieved. Human review is required."
                ),
            }

        top_score = cases[0]["similarity_score"]
        evidence_sufficient = top_score >= self.threshold

        if evidence_sufficient:
            message = (
                "Relevant evidence was found in the fixed case corpus."
            )
        else:
            message = (
                "The retrieved evidence is too weak. "
                "Human review is required."
            )

        return {
            "retrieved_cases": cases,
            "top_score": top_score,
            "threshold": self.threshold,
            "evidence_sufficient": evidence_sufficient,
            "abstain": not evidence_sufficient,
            "message": message,
        }