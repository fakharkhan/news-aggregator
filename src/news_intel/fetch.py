from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, List, Optional

import feedparser
import trafilatura
from dateutil import parser as date_parser
from trafilatura.settings import use_config


@dataclass
class FetchedArticle:
    id: str
    title: str
    url: str
    source: str
    published_at: Optional[datetime]
    content: Optional[str]


def _hash_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]


def _safe_parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        dt = date_parser.parse(date_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _download_main_text(url: str, timeout: int = 20) -> Optional[str]:
    # Configure trafilatura for speed and reliability
    config = use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", str(timeout))
    config.set("DEFAULT", "MIN_OUTPUT_SIZE", "200")
    try:
        downloaded = trafilatura.fetch_url(url, no_ssl=True)
        if not downloaded:
            return None
        result = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_images=False,
            favor_recall=True,
            config=config,
        )
        return result
    except Exception:
        return None


def fetch_from_feeds(feeds: Iterable[tuple[str, str]]) -> List[FetchedArticle]:
    """
    Pull latest entries from a list of (source_name, feed_url).
    """
    articles: List[FetchedArticle] = []
    for source_name, feed_url in feeds:
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries:
            link = getattr(entry, "link", None) or getattr(entry, "id", None)
            title = getattr(entry, "title", None) or "(untitled)"
            if not link:
                # Skip items without a canonical URL
                continue
            article_id = _hash_id(link)
            published = _safe_parse_date(
                getattr(entry, "published", None) or getattr(entry, "updated", None)
            )
            # Basic throttle to avoid hammering sources
            time.sleep(0.1)
            main_text = _download_main_text(link)
            articles.append(
                FetchedArticle(
                    id=article_id,
                    title=title.strip(),
                    url=link,
                    source=source_name,
                    published_at=published,
                    content=main_text,
                )
            )
    return articles

