from __future__ import annotations

import os
from datetime import date, datetime, timezone
from pathlib import Path
from typing import List, Tuple

import typer
from rich.console import Console
from rich.table import Table

from .brief import render_daily_brief_md
from .classify import classify_text
from .config import SourceFeed, load_topics_config
from .fetch import FetchedArticle, fetch_from_feeds
from .storage import (
    DB_PATH_DEFAULT,
    ensure_db,
    get_articles_for_day,
    save_daily_brief,
    set_article_summary_and_category,
    upsert_articles,
)
from .summarize import Summarizer
from .sheets_export import export_daily_to_sheet
from .manifest import update_daily_manifest

app = typer.Typer(add_completion=False)
console = Console()


def _today_utc() -> date:
    return datetime.now(tz=timezone.utc).date()


@app.command("init-db")
def init_db(db_path: str = typer.Option(DB_PATH_DEFAULT, help="SQLite DB path")):
    ensure_db(db_path)
    console.print(f"[green]Initialized DB at[/green] {db_path}")


@app.command("ingest")
def ingest(
    db_path: str = typer.Option(DB_PATH_DEFAULT, help="SQLite DB path"),
    config_path: str = typer.Option("config/topics.yaml", help="Topics YAML config"),
):
    cfg = load_topics_config(config_path)
    feeds: List[Tuple[str, str]] = [(f.name, f.url) for f in cfg.feeds]
    if not feeds:
        console.print("[yellow]No feeds configured. Edit config/topics.yaml[/yellow]")
        raise typer.Exit(code=1)
    console.print(f"[cyan]Fetching from {len(feeds)} feed(s)...[/cyan]")
    arts: List[FetchedArticle] = fetch_from_feeds(feeds)
    conn = ensure_db(db_path)
    rows = []
    for a in arts:
        rows.append(
            (
                a.id,
                a.title,
                a.url,
                a.source,
                a.published_at.isoformat() if a.published_at else None,
                a.content,
            )
        )
    upsert_articles(conn, rows)
    console.print(f"[green]Ingested {len(rows)} article(s).[/green]")


@app.command("summarize")
def summarize_cmd(
    db_path: str = typer.Option(DB_PATH_DEFAULT, help="SQLite DB path"),
    config_path: str = typer.Option("config/topics.yaml", help="Topics YAML config"),
    day: str = typer.Option(None, help="YYYY-MM-DD; default today (UTC)"),
):
    d = date.fromisoformat(day) if day else _today_utc()
    cfg = load_topics_config(config_path)
    conn = ensure_db(db_path)
    articles = get_articles_for_day(conn, d)
    if not articles:
        console.print("[yellow]No articles for selected day.[/yellow]")
        raise typer.Exit(code=0)
    summarizer = Summarizer()
    used_model = "fallback"
    updated = 0
    for row in articles:
        if not row["content"]:
            continue
        res = summarizer.summarize(row["title"], row["content"])
        used_model = res.model
        cl = classify_text(f"{row['title']}\n\n{row['content']}", cfg)
        set_article_summary_and_category(
            conn, row["id"], res.content, cl.category, ", ".join(cl.matched_topics)
        )
        updated += 1
    console.print(f"[green]Summarized {updated} article(s) using {used_model}.[/green]")


@app.command("brief")
def brief_cmd(
    db_path: str = typer.Option(DB_PATH_DEFAULT, help="SQLite DB path"),
    out_dir: str = typer.Option("docs/daily", help="Where to write the Markdown brief"),
    day: str = typer.Option(None, help="YYYY-MM-DD; default today (UTC)"),
    export_sheet: bool = typer.Option(False, help="Also export to Google Sheet if configured"),
    spreadsheet_name: str = typer.Option(
        "News Intelligence Briefs", help="Target Google Spreadsheet name"
    ),
):
    d = date.fromisoformat(day) if day else _today_utc()
    conn = ensure_db(db_path)
    rows = get_articles_for_day(conn, d)
    articles = [dict(r) for r in rows]
    md = render_daily_brief_md(d, articles)
    save_daily_brief(conn, d, md)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(out_dir) / f"{d.isoformat()}.md"
    out_path.write_text(md, encoding="utf-8")
    console.print(f"[green]Wrote brief:[/green] {out_path}")
    manifest = update_daily_manifest(conn, out_dir)
    console.print(f"[blue]Updated manifest:[/blue] {manifest}")
    if export_sheet:
        url = export_daily_to_sheet(spreadsheet_name, d.isoformat(), md)
        if url:
            console.print(f"[cyan]Updated Google Sheet:[/cyan] {url}")
        else:
            console.print("[yellow]Google Sheets export skipped (not configured).[/yellow]")


@app.command("run-daily")
def run_daily(
    db_path: str = typer.Option(DB_PATH_DEFAULT, help="SQLite DB path"),
    config_path: str = typer.Option("config/topics.yaml", help="Topics YAML config"),
    out_dir: str = typer.Option("docs/daily", help="Where to write the Markdown brief"),
    export_sheet: bool = typer.Option(False, help="Also export to Google Sheet if configured"),
    spreadsheet_name: str = typer.Option(
        "News Intelligence Briefs", help="Target Google Spreadsheet name"
    ),
):
    # Call subcommands directly in-process
    ingest(db_path=db_path, config_path=config_path)  # type: ignore[arg-type]
    summarize_cmd(db_path=db_path, config_path=config_path, day=None)  # type: ignore[arg-type]
    brief_cmd(  # type: ignore[arg-type]
        db_path=db_path,
        out_dir=out_dir,
        day=None,
        export_sheet=export_sheet,
        spreadsheet_name=spreadsheet_name,
    )


def main():
    app()


if __name__ == "__main__":
    main()

