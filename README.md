# sru-verifier

A small tool for collecting SRU bug details and guiding package verification runs in a sandboxed environment.


# 1. Fire up your Python script to pull the bug and generate 'test-plans/bug-2147525.json'
uv run sru-verifier bug 2147525

# 2. Spin up the sandboxed environment
workshop launch "sru-env"

# 3. Authenticate Copilot on the first run (persists between workshop updates)
workshop exec sru-env -- copilot auth

# 4. Hand off execution to the agent, specifying package name, series, and bug id
workshop run sru-env execute-sru-test "wget2" "noble" "2147525"
