### Personal Strategic News Intelligence System

This system aggregates news from curated RSS feeds, extracts full-text content, summarizes it with AI, classifies it into strategic categories, and produces a single-page Daily Intelligence Brief in Markdown under `docs/daily/`.

- **Aggregation**: RSS via `feedparser`, article text via `trafilatura`
- **Summarization**: OpenAI (configurable, with no-key fallback)
- **Classification**: Heuristics + topic keyword matching
- **Output**: Markdown brief with sections and links; daily archive

#### Sections
- International Affairs
- Regional
- Pakistan (Local)
- Geopolitics & Power Shifts
- Economy & Technology

The pipeline can run locally or on CI. It stores raw items, summaries, and briefs in `data/news.db` (SQLite).

