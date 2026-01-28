from __future__ import annotations

from typing import List

from .models import Detection, SecurityEvent


BURST_THRESHOLD = 5


def analyze_event(event: SecurityEvent, recent_failures: int) -> Detection:
    indicators: List[str] = []
    risk_score = event.severity

    if event.event_type in {"auth_failure", "privilege_escalation"}:
        indicators.append("authentication anomaly")
        risk_score += 10

    if event.source_ip and event.source_ip.startswith("10."):
        indicators.append("internal source")
        risk_score -= 5

    if recent_failures >= BURST_THRESHOLD:
        indicators.append("burst of failures")
        risk_score += 20

    risk_score = max(0, min(risk_score, 100))

    summary = _build_summary(event, indicators, risk_score)
    return Detection(
        event=event,
        risk_score=risk_score,
        summary=summary,
        indicators=indicators,
    )


def _build_summary(event: SecurityEvent, indicators: List[str], score: int) -> str:
    details = ", ".join(indicators) if indicators else "no obvious indicators"
    ip_info = f" from {event.source_ip}" if event.source_ip else ""
    return f"{score}/100 – {event.event_type} detected{ip_info} ({details})"
