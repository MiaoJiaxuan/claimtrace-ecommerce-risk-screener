"""Load the case corpus and rank evidence by multilingual cosine similarity."""

from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_MODEL_NAME = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


class CaseRetriever:
    """Retrieve similar enforcement cases for one Chinese claim."""

    def __init__(
        self,
        sources_path: str = "data/sources.csv",
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        self.sources_path = Path(sources_path)

        if not self.sources_path.exists():
            raise FileNotFoundError(
                f"Case file was not found: {self.sources_path}"
            )

        self.cases = pd.read_csv(self.sources_path)

        required_columns = {
            "case_id",
            "publisher",
            "publish_date",
            "title",
            "case_text",
            "risk_type",
            "source_url",
        }

        missing_columns = required_columns - set(self.cases.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        if self.cases.empty:
            raise ValueError("The case file does not contain any cases.")

        self.model = SentenceTransformer(model_name)

        documents = (
            self.cases["title"].fillna("")
            + " "
            + self.cases["case_text"].fillna("")
        ).tolist()

        self.case_embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
        )

    def retrieve(self, claim: str, top_k: int = 3) -> list[dict]:
        """Return the most similar cases and their similarity scores."""

        cleaned_claim = claim.strip()

        if not cleaned_claim:
            return []

        claim_embedding = self.model.encode(
            [cleaned_claim],
            normalize_embeddings=True,
        )

        scores = cosine_similarity(
            claim_embedding,
            self.case_embeddings,
        )[0]

        result_count = min(top_k, len(self.cases))
        ranked_indices = scores.argsort()[::-1][:result_count]

        results = []

        for index in ranked_indices:
            case = self.cases.iloc[index]

            results.append(
                {
                    "case_id": case["case_id"],
                    "title": case["title"],
                    "case_text": case["case_text"],
                    "risk_type": case["risk_type"],
                    "source_url": case["source_url"],
                    "similarity_score": round(float(scores[index]), 4),
                }
            )

        return results
