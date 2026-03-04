### Operations

#### Local cron (daily)
Example crontab (runs at 06:00 UTC daily):
```bash
0 6 * * * cd /path/to/repo && /path/to/venv/bin/python -m news_intel.cli run-daily >> logs/daily.log 2>&1
```

#### GitHub Actions (scheduled)
Create `.github/workflows/daily-intel.yml`:
```yaml
name: Daily Intelligence

on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch: {}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run pipeline
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          OPENAI_MODEL: gpt-4o-mini
        run: |
          python -m news_intel.cli init-db
          python -m news_intel.cli run-daily
      - name: Commit daily brief
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add docs/daily data/news.db
          if git diff --cached --quiet; then
            echo "No changes to commit."
          else
            TS=$(date -u +'%Y-%m-%d')
            git commit -m "chore: add daily brief ${TS}"
            git push
          fi
```

Secrets:
- `OPENAI_API_KEY` (optional; enables high-quality summaries)

#### Creating a new GitHub repo
If the assistant cannot create repos automatically due to token scope, run:

```bash
scripts/create_repo_with_pat.sh my-username my-private-repo
```

Where `GITHUB_PAT` is exported in your environment with `repo` scope.

