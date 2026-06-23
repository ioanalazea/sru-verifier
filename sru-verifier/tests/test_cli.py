from sru_verifier.cli import _extract_affected_packages


class _Task:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class _Target:
    def __init__(self, name: str):
        self.name = name


class _Bug:
    def __init__(self, tasks):
        self.bug_tasks = tasks


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
