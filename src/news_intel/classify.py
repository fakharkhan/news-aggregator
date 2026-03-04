from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .config import Category, TopicsConfig


@dataclass
class Classification:
    category: str
    matched_keywords: List[str]
    matched_topics: List[str]


def _lower_words(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z\-\&]+", text.lower())
    return tokens


def _match_keywords(text: str, keywords: List[str]) -> List[str]:
    lower = text.lower()
    matches = []
    for kw in keywords:
        if kw.lower() in lower:
            matches.append(kw)
    return matches


def classify_text(
    text: str,
    config: TopicsConfig,
    default_category: str = "International Affairs",
) -> Classification:
    """
    Heuristic classification across configured categories and user topics.
    """
    matched_topics = _match_keywords(text, config.topics)
    category_scores: List[Tuple[str, int, List[str]]] = []
    for name, cat in config.categories.items():
        kws = cat.keywords if isinstance(cat, Category) else []
        hits = _match_keywords(text, kws)
        score = len(hits)
        category_scores.append((name, score, hits))

    # Prefer Pakistan (Local) if "Pakistan" appears anywhere
    if "pakistan" in text.lower():
        pak = config.categories.get("Pakistan (Local)")
        pak_hits = _match_keywords(text, pak.keywords if pak else ["Pakistan"])
        return Classification("Pakistan (Local)", pak_hits, matched_topics)

    # Pick the category with highest score, fallback
    category_scores.sort(key=lambda t: t[1], reverse=True)
    top_name, top_score, top_hits = category_scores[0]
    chosen = top_name if top_score > 0 else default_category
    matched = top_hits if top_score > 0 else []
    return Classification(chosen, matched, matched_topics)

