from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import yaml


@dataclass
class Category:
    name: str
    keywords: List[str] = field(default_factory=list)


@dataclass
class SourceFeed:
    name: str
    url: str
    category: Optional[str] = None
    language: Optional[str] = "en"
    region: Optional[str] = None


@dataclass
class TopicsConfig:
    # Free-form topics/questions/keywords to prioritize
    topics: List[str] = field(default_factory=list)
    # Static categories and their indicative keywords
    categories: Dict[str, Category] = field(default_factory=dict)
    # RSS/Atom feeds to ingest
    feeds: List[SourceFeed] = field(default_factory=list)


DEFAULT_CATEGORIES: Dict[str, Category] = {
    "International Affairs": Category(
        name="International Affairs",
        keywords=[
            "UN",
            "diplomat",
            "sanctions",
            "treaty",
            "conflict",
            "ceasefire",
            "bilateral",
            "multilateral",
            "NATO",
            "EU",
        ],
    ),
    "Regional": Category(
        name="Regional",
        keywords=[
            "South Asia",
            "Middle East",
            "Asia-Pacific",
            "Gulf",
            "neighbors",
        ],
    ),
    "Pakistan (Local)": Category(
        name="Pakistan (Local)",
        keywords=[
            "Pakistan",
            "Islamabad",
            "Lahore",
            "Karachi",
            "Peshawar",
            "Sindh",
            "Punjab",
            "KP",
            "Balochistan",
        ],
    ),
    "Geopolitics & Power Shifts": Category(
        name="Geopolitics & Power Shifts",
        keywords=[
            "superpower",
            "influence",
            "strategic",
            "alliances",
            "power balance",
            "hegemony",
            "deterrence",
            "BRICS",
            "Quad",
            "AUKUS",
        ],
    ),
    "Economy & Technology": Category(
        name="Economy & Technology",
        keywords=[
            "inflation",
            "GDP",
            "markets",
            "exports",
            "imports",
            "trade",
            "startup",
            "AI",
            "semiconductor",
            "fintech",
            "energy",
        ],
    ),
}


def _load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_topics_config(config_path: Optional[str] = None) -> TopicsConfig:
    """
    Load topics configuration from YAML, falling back to defaults.
    """
    if config_path is None:
        config_path = os.getenv("NEWS_INTEL_TOPICS", "config/topics.yaml")

    if not os.path.exists(config_path):
        # Return defaults if no file yet
        return TopicsConfig(
            topics=[],
            categories=DEFAULT_CATEGORIES,
            feeds=[],
        )

    raw = _load_yaml(config_path)
    topics: List[str] = raw.get("topics", []) or []

    # Load/merge categories
    categories_raw = raw.get("categories", {}) or {}
    categories: Dict[str, Category] = {k: v for k, v in DEFAULT_CATEGORIES.items()}
    for name, data in categories_raw.items():
        if isinstance(data, dict):
            keywords = data.get("keywords", []) or []
        elif isinstance(data, list):
            keywords = data
        else:
            keywords = []
        categories[name] = Category(name=name, keywords=keywords)

    feeds_raw = raw.get("feeds", []) or []
    feeds: List[SourceFeed] = []
    for f in feeds_raw:
        feeds.append(
            SourceFeed(
                name=f.get("name") or f.get("url", "unknown"),
                url=f["url"],
                category=f.get("category"),
                language=f.get("language", "en"),
                region=f.get("region"),
            )
        )

    return TopicsConfig(topics=topics, categories=categories, feeds=feeds)

