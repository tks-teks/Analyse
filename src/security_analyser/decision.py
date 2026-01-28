from __future__ import annotations

from typing import List

from .models import Decision, Detection


HIGH_RISK = 80
MEDIUM_RISK = 60


def decide(detection: Detection) -> Decision:
    score = detection.risk_score
    if score >= HIGH_RISK:
        action = "Bloquer l'IP et notifier l'équipe SOC immédiatement"
        steps = [
            "Activer une règle de blocage temporaire (1h)",
            "Imposer MFA pour l'utilisateur concerné",
            "Conserver les logs pour analyse forensique",
        ]
    elif score >= MEDIUM_RISK:
        action = "Surveiller activement et demander une validation MFA"
        steps = [
            "Renforcer la journalisation sur la source",
            "Alerter l'équipe SOC en mode veille",
            "Planifier un scan de vulnérabilités ciblé",
        ]
    else:
        action = "Surveillance standard"
        steps = [
            "Conserver l'événement pour corrélation future",
            "Vérifier les seuils d'alerte si récurrence",
        ]

    return Decision(
        detection=detection,
        recommended_action=action,
        prevention_steps=steps,
    )
