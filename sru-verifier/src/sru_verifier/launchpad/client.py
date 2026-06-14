# launchpad/client.py

from launchpadlib.launchpad import Launchpad

def get_launchpad():
    return Launchpad.login_anonymously(
        "sru-verifier",
        "production"
    )

def get_bug(bug_id: int):
    lp = get_launchpad()
    return lp.bugs[bug_id]