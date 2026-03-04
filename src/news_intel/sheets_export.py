from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterable, List, Optional

import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


def _get_gspread_client() -> Optional[gspread.Client]:
    keyfile = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not keyfile or not os.path.exists(keyfile):
        return None
    creds = Credentials.from_service_account_file(keyfile, scopes=SCOPE)
    return gspread.authorize(creds)


def export_daily_to_sheet(
    spreadsheet_name: str,
    day_iso: str,
    brief_md: str,
    worksheet_title: str = "Daily Briefs",
) -> Optional[str]:
    """
    Write the daily brief markdown into a Google Sheet.
    Returns URL on success, or None if not configured.
    """
    client = _get_gspread_client()
    if not client:
        return None
    try:
        try:
            sh = client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            sh = client.create(spreadsheet_name)
        try:
            ws = sh.worksheet(worksheet_title)
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(title=worksheet_title, rows="1000", cols="3")
            ws.update("A1:C1", [["Date", "Section/Title", "Content"]])
        # Simple serialization: each H2/H3 section as a row
        rows: List[List[str]] = []
        current_section = ""
        for line in brief_md.splitlines():
            if line.startswith("## "):
                current_section = line.replace("## ", "").strip()
            elif line.startswith("### "):
                title = line.replace("### ", "").strip()
                rows.append([day_iso, f"{current_section} — {title}", ""])  # title row
            elif line.strip() and not line.startswith("#"):
                if rows:
                    # append content to last row
                    if rows[-1][2]:
                        rows[-1][2] += "\n" + line
                    else:
                        rows[-1][2] = line
        if rows:
            ws.append_rows(rows, value_input_option="RAW")
        return sh.url
    except Exception:
        return None

