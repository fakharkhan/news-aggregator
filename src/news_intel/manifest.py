from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

import sqlite3


def _list_days(conn: sqlite3.Connection) -> List[str]:
    cur = conn.execute("SELECT day FROM daily_briefs ORDER BY day DESC;")
    return [r[0] for r in cur.fetchall()]


def _category_counts_for_day(conn: sqlite3.Connection, day_iso: str) -> Dict[str, int]:
    cur = conn.execute(
        """
        SELECT category, COUNT(*) as c
        FROM articles
        WHERE date(COALESCE(published_at, created_at)) = date(?)
        GROUP BY category;
        """,
        (day_iso,),
    )
    result: Dict[str, int] = {}
    for cat, c in cur.fetchall():
        result[cat or "International Affairs"] = int(c)
    return result


def _topics_counts_for_day(conn: sqlite3.Connection, day_iso: str) -> Dict[str, int]:
    cur = conn.execute(
        """
        SELECT topics
        FROM articles
        WHERE date(COALESCE(published_at, created_at)) = date(?)
          AND topics IS NOT NULL AND LENGTH(TRIM(topics)) > 0;
        """,
        (day_iso,),
    )
    counter: Counter[str] = Counter()
    for (topics_str,) in cur.fetchall():
        for t in (topics_str or "").split(","):
            t = t.strip()
            if t:
                counter[t] += 1
    return dict(counter.most_common(20))


def update_daily_manifest(conn: sqlite3.Connection, out_dir: str = "docs/daily") -> str:
    """
    Write docs/daily/index.json that lists available days and basic analytics.
    Returns the path to the manifest file.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    days = _list_days(conn)
    records: List[Dict] = []
    for day_iso in days:
        records.append(
            {
                "day": day_iso,
                "md_path": f"{day_iso}.md",
                "categories": _category_counts_for_day(conn, day_iso),
                "topics": _topics_counts_for_day(conn, day_iso),
            }
        )
    manifest_path = Path(out_dir) / "index.json"
    manifest_path.write_text(json.dumps({"days": records}, indent=2), encoding="utf-8")
    return str(manifest_path)

