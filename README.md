Personal Strategic News Intelligence System
===========================================

This repository contains a lightweight, automatable system that ingests news from curated RSS feeds, extracts and summarizes content with AI, classifies items into strategic categories, and produces a concise 1‑page Daily Intelligence Brief in Markdown under `docs/daily/`.

Key features:
- AI-based summaries per article (OpenAI, with graceful fallback if no key)
- Structured sections: International Affairs, Regional, Pakistan (Local), Geopolitics & Power Shifts, Economy & Technology
- Automatic daily run via a single CLI or GitHub Actions
- Archive of daily briefs by date in `docs/daily/`
- Topic filtering and category tuning via `config/topics.yaml`

Quickstart
----------
1) Create and activate a Python 3.11+ environment.
2) Install dependencies:
```bash
pip install -r requirements.txt
```
3) Configure topics and feeds in `config/topics.yaml`.
4) Optionally set your OpenAI API key (for best summaries):
```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini
```
5) Run the daily pipeline:
```bash
python -m news_intel.cli init-db
python -m news_intel.cli run-daily
```
6) Find your brief at `docs/daily/YYYY-MM-DD.md`.

Automation
----------
- See `docs/news-intel/operations.md` for GitHub Actions and cron examples.
- Add a PAT with `repo` scope to let a CI create/update a private repo if desired.

Customization
-------------
- Edit `config/topics.yaml` to change categories, topics, and feeds.
- The brief composer is in `src/news_intel/brief.py`.
- Classification heuristics live in `src/news_intel/classify.py`.

