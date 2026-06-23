from sru_verifier.parser.sru import extract_section, parse_sru_sections


def test_extract_section_from_bracket_headers() -> None:
    text = """[Impact]
Kernel panic on startup.

[Test Plan]
Boot the system and verify logs.

[Regression Potential]
Low risk.
"""

    assert extract_section(text, "Impact") == "Kernel panic on startup."
    assert extract_section(text, "Test Plan") == "Boot the system and verify logs."


def test_parse_sru_sections_returns_known_keys() -> None:
    text = """## Impact
Bluetooth fails intermittently.

## Test Plan
Run repeated reconnect cycles.
"""

    parsed = parse_sru_sections(text, ["Impact", "Test Plan", "Regression Potential"])
    assert parsed["Impact"] == "Bluetooth fails intermittently."
    assert parsed["Test Plan"] == "Run repeated reconnect cycles."
    assert parsed["Regression Potential"] is None


def test_parse_sru_sections_is_case_insensitive_for_all_default_sections() -> None:
    text = """[impact]
Impact details.

[test plan]
Test plan details.

[REGRESSION POTENTIAL]
Regression details.

[where Problems could occur]
Where details.

[oThEr iNfO]
Other details.
"""

    parsed = parse_sru_sections(text)

    assert parsed["Impact"] == "Impact details."
    assert parsed["Test Plan"] == "Test plan details."
    assert parsed["Regression Potential"] == "Regression details."
    assert parsed["Where problems could occur"] == "Where details."
    assert parsed["Other Info"] == "Other details."


def test_parse_sru_sections_can_include_full_description() -> None:
    text = """[Impact]
Something broke.
"""

    parsed = parse_sru_sections(text, include_full_description=True)

    assert parsed["Impact"] == "Something broke."
    assert parsed["Full Description"] == text.strip()
