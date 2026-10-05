"""A Local-harness reminder, deliberately independent of transcript contents."""

import json
import sys


def reminder(event: dict) -> dict:
    if event.get("hook_event_name") != "Stop":
        raise ValueError("Expected a VS Code Local Stop event.")
    return {
        "systemMessage": (
            "Before opening a PR, run /speckit.adas.capture and review a sanitized "
            "docs/session-notes record. Share only explicitly approved decisions "
            "and observed test evidence; never raw transcripts or hidden reasoning."
        )
    }


if __name__ == "__main__":
    print(json.dumps(reminder(json.load(sys.stdin))))
