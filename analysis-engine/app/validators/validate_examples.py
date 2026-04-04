from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from app.models.event_models import PrometheusEvent


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    examples_dir = repo_root / "schemas" / "examples"

    valid_files = [
        "ssh.session_start.valid.json",
        "ssh.auth_attempt.valid.json",
        "ssh.auth_result.valid.json",
        "ssh.connection_closed.valid.json",
    ]

    invalid_files = [
        "invalid.missing_session_id.json",
    ]

    print("=== VALIDATING VALID EXAMPLES ===")
    for filename in valid_files:
        file_path = examples_dir / filename
        with file_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        try:
            event = PrometheusEvent.model_validate(payload)
            print(f"[OK] {filename} -> event_type={event.event_type}, session_id={event.session_id}")
        except ValidationError as exc:
            print(f"[FAIL] {filename} should be valid but failed")
            print(exc)
            raise

    print()
    print("=== VALIDATING INVALID EXAMPLES ===")
    for filename in invalid_files:
        file_path = examples_dir / filename
        with file_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        try:
            PrometheusEvent.model_validate(payload)
            print(f"[FAIL] {filename} should be invalid but passed")
            raise SystemExit(1)
        except ValidationError as exc:
            print(f"[OK] {filename} correctly failed validation")
            print(exc.errors()[0])

    print()
    print("[OK] Example validation completed successfully.")


if __name__ == "__main__":
    main()