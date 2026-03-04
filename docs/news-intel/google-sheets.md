### Optional: Google Sheets export

You can export each day's brief to a Google Sheet for simple browsing/filtering.

1) Create a Google Cloud Project and a Service Account with Drive/Sheets access.
2) Download the Service Account JSON key to your machine/repo host.
3) Set:
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON=/absolute/path/to/key.json
```
4) Share the target Sheet (or create permission) with the Service Account email.
5) Run:
```bash
python -m news_intel.cli brief --export-sheet --spreadsheet-name "News Intelligence Briefs"
```

In CI, store the service account JSON as an Actions Secret and write it to a file at runtime before executing the export step.

