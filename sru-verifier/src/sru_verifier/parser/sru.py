import re


# Common SRU template sections used in bug descriptions.
DEFAULT_SRU_SECTIONS = [
    "Impact",
    "Test Plan",
    "Regression Potential",
    "Where problems could occur",
    "Other Info",
]


def _normalize_section(section: str) -> str:
    return section.strip().strip("[]").strip().lower()


def _header_name(line: str) -> str | None:
    candidate = line.strip()
    if not candidate:
        return None

    candidate = candidate.lstrip("#").strip()
    if candidate.endswith(":"):
        candidate = candidate[:-1].strip()
    if candidate.startswith("[") and candidate.endswith("]"):
        candidate = candidate[1:-1].strip()

    if not re.match(r"^[A-Za-z0-9][\w /\-]*$", candidate):
        return None

    return candidate


def _is_header_line(line: str) -> bool:
    return _header_name(line) is not None


def _line_matches_section(line: str, section: str) -> bool:
    header = _header_name(line)
    if header is None:
        return False
    return _normalize_section(header) == _normalize_section(section)


def extract_section(text: str, section: str) -> str | None:
    lines = text.splitlines()
    section_idx = None

    for idx, line in enumerate(lines):
        if _line_matches_section(line, section):
            section_idx = idx
            break

    if section_idx is None:
        return None

    value_lines: list[str] = []
    for line in lines[section_idx + 1 :]:
        if _is_header_line(line):
            break
        value_lines.append(line)

    value = "\n".join(value_lines).strip()
    return value or None


def parse_sru_sections(
    text: str,
    sections: list[str] | None = None,
    include_full_description: bool = False,
) -> dict[str, str | None]:
    selected_sections = sections or DEFAULT_SRU_SECTIONS
    parsed = {name: extract_section(text, name) for name in selected_sections}

    if include_full_description:
        parsed["Full Description"] = text.strip() or None

    return parsed
