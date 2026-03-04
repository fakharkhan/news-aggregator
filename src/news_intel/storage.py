from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


DB_PATH_DEFAULT = "data/news.db"


def _utcnow() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def ensure_db(path: str = DB_PATH_DEFAULT) -> sqlite3.Connection:
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            source TEXT NOT NULL,
            published_at TEXT,
            content TEXT,
            summary TEXT,
            category TEXT,
            topics TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_articles_published_at
            ON articles (published_at);

        CREATE TABLE IF NOT EXISTS daily_briefs (
            day TEXT PRIMARY KEY,
            brief_md TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    return conn


def upsert_articles(
    conn: sqlite3.Connection, rows: Sequence[Tuple[str, str, str, str, Optional[str], Optional[str]]]
) -> None:
    """
    Upsert articles by id.
    rows: (id, title, url, source, published_at_iso, content)
    """
    now = _utcnow()
    for row in rows:
        (aid, title, url, source, published_at, content) = row
        conn.execute(
            """
            INSERT INTO articles (id, title, url, source, published_at, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                url=excluded.url,
                source=excluded.source,
                published_at=excluded.published_at,
                content=COALESCE(articles.content, excluded.content),
                updated_at=excluded.updated_at;
            """,
            (aid, title, url, source, published_at, content, now, now),
        )
    conn.commit()


def set_article_summary_and_category(
    conn: sqlite3.Connection, article_id: str, summary: str, category: str, topics: str
) -> None:
    now = _utcnow()
    conn.execute(
        """
        UPDATE articles
        SET summary = ?, category = ?, topics = ?, updated_at = ?
        WHERE id = ?;
        """,
        (summary, category, topics, now, article_id),
    )
    conn.commit()


def get_articles_for_day(conn: sqlite3.Connection, d: date) -> List[sqlite3.Row]:
    start = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc).isoformat()
    end = datetime(d.year, d.month, d.day, 23, 59, 59, tzinfo=timezone.utc).isoformat()
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        """
        SELECT * FROM articles
        WHERE published_at IS NULL OR (published_at >= ? AND published_at <= ?)
        ORDER BY COALESCE(published_at, created_at) DESC;
        """,
        (start, end),
    )
    return list(cur.fetchall())


def save_daily_brief(conn: sqlite3.Connection, d: date, brief_md: str) -> None:
    now = _utcnow()
    key = d.isoformat()
    conn.execute(
        """
        INSERT INTO daily_briefs(day, brief_md, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(day) DO UPDATE SET brief_md=excluded.brief_md, updated_at=excluded.updated_at;
        """,
        (key, brief_md, now, now),
    )
    conn.commit()


def get_daily_brief(conn: sqlite3.Connection, d: date) -> Optional[str]:
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT brief_md FROM daily_briefs WHERE day = ?;", (d.isoformat(),))
    row = cur.fetchone()
    return row["brief_md"] if row else None

