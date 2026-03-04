### Setup

1) Python environment (3.11+ recommended), then:
```bash
pip install -r requirements.txt
```

2) Configure topics and feeds in `config/topics.yaml`. You can:
- Add/remove feeds
- Adjust category keywords
- Add personal topics, questions, and keywords

3) (Optional) Enable AI summaries:
```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini
```

4) Initialize the database:
```bash
python -m news_intel.cli init-db
```

5) Run the full daily pipeline:
```bash
python -m news_intel.cli run-daily
```

Outputs are written to `docs/daily/YYYY-MM-DD.md`.

