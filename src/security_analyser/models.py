from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class SecurityEvent:
    raw: str
    event_type: str
    severity: int
    source_ip: Optional[str] = None
    username: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Detection:
    event: SecurityEvent
    risk_score: int
    summary: str
    indicators: List[str]


@dataclass
class Decision:
    detection: Detection
    recommended_action: str
    prevention_steps: List[str]
