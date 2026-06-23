# sru-verifier

A small tool for collecting SRU bug details and guiding package verification runs in a sandboxed environment.


# 1. Fire up your Python script to pull the bug and generate 'sru_test_plan.txt'
uv run sru-verifier bug 2147525 --json

# 2. Spin up the sandboxed environment
workshop launch "sru-env"

# 3. Authenticate Copilot on the first run (persists between workshop updates)
workshop exec sru-env -- copilot auth

# 4. Hand off execution to the agent, specifying package name and series
workshop run sru-env execute-sru-test "wget2" "noble"