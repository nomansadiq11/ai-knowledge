from typing import List, Dict
import re
import numpy as np


def _split_sentences(text: str) -> List[str]:
    # Simple sentence splitter; avoids extra deps
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def verify_answer(answer: str, sources: List[object], embeddings) -> Dict[str, object]:
    """
    Verify answer faithfulness against source documents using embedding similarity.
    - Splits the answer into sentences.
    - Computes cosine similarity between each sentence and all source chunks.
    - Produces coverage metrics and flags low-supported sentences.

    Returns: dict with keys: coverage_score, max_sim, low_coverage_sentences, flagged, details
    """
    sentences = _split_sentences(answer)
    if not sentences or not sources:
        return {
            "coverage_score": 0.0,
            "max_sim": 0.0,
            "low_coverage_sentences": len(sentences),
            "flagged": True,
            "details": [],
        }

    # Embed answer sentences and source chunks
    sent_vecs = [embeddings.embed_query(s) for s in sentences]
    src_texts = [getattr(doc, "page_content", str(doc)) for doc in sources]
    src_vecs = [embeddings.embed_query(t) for t in src_texts]

    # Per-sentence max similarity across sources
    per_sentence_max = []
    for sv in sent_vecs:
        sims = [cosine_sim(np.array(sv), np.array(tv)) for tv in src_vecs]
        per_sentence_max.append(max(sims) if sims else 0.0)

    coverage = float(np.mean(per_sentence_max)) if per_sentence_max else 0.0
    max_sim = float(np.max(per_sentence_max)) if per_sentence_max else 0.0

    # Thresholds (tunable)
    LOW_SENT_THRESHOLD = 0.35
    FLAG_THRESHOLD = 0.30

    low_supported = sum(1 for s in per_sentence_max if s < LOW_SENT_THRESHOLD)
    flagged = coverage < FLAG_THRESHOLD

    return {
        "coverage_score": round(coverage, 3),
        "max_sim": round(max_sim, 3),
        "low_coverage_sentences": low_supported,
        "flagged": flagged,
        "details": per_sentence_max,
    }
