from pathlib import Path

from typer.testing import CliRunner

from sru_verifier import cli
from sru_verifier.cli import _extract_affected_packages, _json_output_path, app


runner = CliRunner()


class _Task:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class _Target:
    def __init__(self, name: str):
        self.name = name


class _Bug:
    def __init__(self, tasks, description: str = ""):
        self.bug_tasks = tasks
        self.description = description
        self.title = "Test bug"
        self.web_link = "https://example.test/bugs/1"


def test_extract_affected_packages_prefers_source_package_name() -> None:
    bug = _Bug(
        [
            _Task(sourcepackagename="iproute2", bug_target_name="Ubuntu"),
            _Task(sourcepackagename="iproute2"),
            _Task(sourcepackagename="linux"),
        ]
    )

    assert _extract_affected_packages(bug) == ["iproute2", "linux"]


def test_extract_affected_packages_falls_back_to_target_fields() -> None:
    bug = _Bug(
        [
            _Task(bug_target_name="systemd (Ubuntu)"),
            _Task(target_name="NetworkManager"),
            _Task(target=_Target("snapd")),
            _Task(bug_target_name="Ubuntu"),
        ]
    )

    assert _extract_affected_packages(bug) == ["NetworkManager", "snapd", "systemd"]


def test_json_output_path_uses_dedicated_directory() -> None:
    assert _json_output_path(2147525, Path("test-plans")) == Path("test-plans/bug-2147525.json")


def test_bug_command_writes_bug_specific_json_file(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(cli, "get_bug", lambda bug_id: _Bug([_Task(sourcepackagename="wget2")]))

    result = runner.invoke(app, ["bug", "2147525", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0
    assert "Saved to" in result.stdout
    assert (tmp_path / "bug-2147525.json").exists()
