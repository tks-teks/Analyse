from __future__ import annotations

from dataclasses import dataclass

from .models import Decision


@dataclass
class VoiceAssistant:
    enabled: bool = False

    def notify(self, decision: Decision) -> None:
        if not self.enabled:
            return
        message = self._build_message(decision)
        print(f"[VOICE] {message}")

    def _build_message(self, decision: Decision) -> str:
        score = decision.detection.risk_score
        if score >= 80:
            return (
                "Alerte critique. Action immédiate recommandée pour cet incident."
            )
        if score >= 60:
            return "Alerte modérée. Une surveillance renforcée est conseillée."
        return "Incident faible. Continuer la surveillance standard."
