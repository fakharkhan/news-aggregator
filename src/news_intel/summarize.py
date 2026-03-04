from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - library may not be installed yet
    OpenAI = None  # type: ignore


SUMMARY_SYSTEM_PROMPT = (
    "You are an analyst producing concise, structured intelligence summaries. "
    "Write in clear bullet points, include key facts, actors, numbers, and implications. "
    "Keep each article summary under 120 words. Neutral, analytic tone."
)


@dataclass
class SummaryResult:
    model: str
    content: str


class Summarizer:
    def __init__(self, model: Optional[str] = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY")
        if OpenAI is None:
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key) if api_key else None

    def is_enabled(self) -> bool:
        return self.client is not None

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception),
    )
    def summarize(self, title: str, content: str) -> SummaryResult:
        if not self.client:
            # Fallback: return truncated content if no API key present
            excerpt = (content or "").strip().split("\n")
            excerpt_text = " ".join(excerpt[:4])[:480]
            fallback = f"- {title.strip()}\n- {excerpt_text}..."
            return SummaryResult(model="fallback", content=fallback)

        messages = [
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Article title: {title}\n\nArticle content:\n{content}\n\n"
                "Produce a concise bullet summary with 3-5 bullets.",
            },
        ]
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                temperature=0.2,
            )
            text = resp.choices[0].message.content  # type: ignore[assignment]
            return SummaryResult(model=self.model, content=text or "")
        except Exception as e:
            # Last-resort: same fallback as disabled mode
            excerpt_text = (content or "").strip()[:480]
            return SummaryResult(model="error-fallback", content=f"- {title}\n- {excerpt_text}...")

