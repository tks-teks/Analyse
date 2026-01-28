from __future__ import annotations

import argparse
from collections import deque
from typing import Iterable

from .assistant import VoiceAssistant
from .decision import decide
from .ingest import parse_lines
from .rules import analyze_event


def _read_lines(path: str | None) -> Iterable[str]:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.readlines()
    return iter(input, "")


def run(path: str | None, voice: bool) -> None:
    assistant = VoiceAssistant(enabled=voice)
    recent_failures = deque(maxlen=10)

    for event in parse_lines(_read_lines(path)):
        if event.event_type == "auth_failure":
            recent_failures.append(event)
        detection = analyze_event(event, recent_failures=len(recent_failures))
        decision = decide(detection)

        print(f"[ALERTE] {detection.summary}")
        print(f"Action recommandée : {decision.recommended_action}")
        for step in decision.prevention_steps:
            print(f"- {step}")
        assistant.notify(decision)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Intelligent security log analyzer (prototype)."
    )
    parser.add_argument("--logfile", help="Path to log file", default=None)
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Enable simulated voice assistant output",
    )
    args = parser.parse_args()
    run(args.logfile, args.voice)


if __name__ == "__main__":
    main()
