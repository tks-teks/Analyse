from __future__ import annotations

import json
import re
from typing import Iterable, Iterator

from .models import SecurityEvent

KEYWORDS = {
    "failed login": ("auth_failure", 60),
    "authentication failed": ("auth_failure", 65),
    "sql injection": ("sql_injection", 85),
    "malware": ("malware", 90),
    "ransomware": ("ransomware", 95),
    "privilege escalation": ("privilege_escalation", 80),
}

IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def _extract_ip(text: str) -> str | None:
    match = IP_REGEX.search(text)
    return match.group(0) if match else None


def parse_lines(lines: Iterable[str]) -> Iterator[SecurityEvent]:
    for line in lines:
        line = line.strip()
        if not line:
            continue
        event = _parse_json(line)
        if event:
            yield event
            continue
        yield _parse_text(line)


def _parse_json(line: str) -> SecurityEvent | None:
    if not line.startswith("{"):
        return None
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return None
    event_type = payload.get("event", "generic")
    severity = int(payload.get("severity", 40))
    return SecurityEvent(
        raw=line,
        event_type=event_type,
        severity=severity,
        source_ip=payload.get("source_ip") or payload.get("ip"),
        username=payload.get("user"),
        metadata=payload,
    )


def _parse_text(line: str) -> SecurityEvent:
    lowered = line.lower()
    for keyword, (event_type, severity) in KEYWORDS.items():
        if keyword in lowered:
            return SecurityEvent(
                raw=line,
                event_type=event_type,
                severity=severity,
                source_ip=_extract_ip(line),
            )
    return SecurityEvent(
        raw=line,
        event_type="generic",
        severity=30,
        source_ip=_extract_ip(line),
    )
