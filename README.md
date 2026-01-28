# Intelligent Security Log Analyzer (prototype)

Un système intelligent d'analyse de logs de sécurité qui ne se limite pas aux logs : il
corrèle les signaux, prend des décisions et propose des actions de prévention. Le module
propose aussi un mode d'assistance vocale (simulé) pour faciliter la gestion et
l'interlocution en temps réel.

## Objectifs clés

- **Analyse multi-sources** : ingestion de logs bruts, événements JSON, signaux
  contextuels (ex : IP, pays, type d'appareil).
- **Détection de risques** : règles interprétables + scoring de risque.
- **Décision et prévention** : recommandations d'actions (blocage, MFA,
  surveillance renforcée).
- **Assistance vocale** : synthèse orale (simulée) pour accompagner l'opérateur.

## Démarrage rapide

```bash
python -m security_analyser.cli --logfile sample.log --voice
```

Sans fichier, le CLI lit l'entrée standard :

```bash
cat sample.log | python -m security_analyser.cli --voice
```

## Format de logs pris en charge

- JSON par ligne (`{"event":"login", "status":"fail", ...}`)
- Texte brut : détection par mots-clés (`failed login`, `sql injection`, etc.)

## Exemple de sortie

```
[ALERTE] 84/100 – Suspicious authentication burst from 192.0.2.1
Action recommandée : activer MFA et bloquer l'IP pendant 1h
[VOICE] Alerte critique. Authentifications suspectes détectées.
```

## Structure

- `ingest.py` : parsing et normalisation.
- `rules.py` : règles de détection et enrichissement.
- `decision.py` : scoring et décisions de prévention.
- `assistant.py` : assistance vocale (simulée).
- `cli.py` : interface opérateur.
- `web/` : console holographique 3D (frontend).

## Interface holographique 3D

Une console web immersive met en scène l'assistance vocale sous forme d'hologramme
animé. Elle est conçue pour être branchée à des flux temps réel (alertes, décisions)
et propose des panneaux de situation, des timelines et une visualisation radar.

```bash
cd web
python -m http.server 8000
```

Puis ouvrir <http://localhost:8000> dans le navigateur.

## Notes

Ce prototype est conçu pour être extensible (ajout de connecteurs SIEM, modèles ML,
TTS/STT). Les fonctions sont volontairement simples et compatibles avec l'environnement
standard Python.
