# src/sru_verifier/cli.py

import json
from pathlib import Path

import typer
from .launchpad.client import get_bug
from .parser.sru import parse_sru_sections

app = typer.Typer()


def _extract_affected_packages(bug: object) -> list[str]:
    packages: set[str] = set()

    for task in getattr(bug, "bug_tasks", []) or []:
        name: str | None = None

        for attr in ("sourcepackagename", "source_package_name", "bug_target_name", "target_name"):
            value = getattr(task, attr, None)
            if isinstance(value, str) and value.strip():
                name = value.strip()
                break

        if not name:
            target = getattr(task, "target", None)
            value = getattr(target, "name", None)
            if isinstance(value, str) and value.strip():
                name = value.strip()

        if not name:
            continue

        # Launchpad target names can include extra context, keep just package name.
        cleaned = name.split(" (", 1)[0].strip()
        if cleaned and cleaned.lower() not in {"ubuntu", "debian"}:
            packages.add(cleaned)

    return sorted(packages)

@app.command()
def bug(
    bug_id: int,
    json_output: bool = typer.Option(False, "--json", help="Save bug details to sru_test_plan.txt."),
):
    bug = get_bug(bug_id)

    if json_output:
        description = getattr(bug, "description", "") or ""
        payload = {
            "id": bug_id,
            "title": getattr(bug, "title", None),  #idk if i need this part
            "web_link": getattr(bug, "web_link", None),
            "affected_packages": _extract_affected_packages(bug),
            "sru": parse_sru_sections(description, include_full_description=True),  # maybe this only
        }

        output_path = Path("sru_test_plan.txt")
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        typer.echo(f"Saved to {output_path}")
        return

    print(f"Fetching bug {bug_id}")
    print(bug.title)


if __name__ == "__main__":
    app()