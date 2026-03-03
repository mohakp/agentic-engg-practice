import re


def extract_headers(markdown: str) -> list[tuple[int, str]]:
    """Extract ATX-style markdown headers as (level, text) tuples."""
    headers: list[tuple[int, str]] = []
    header_pattern = re.compile(r"^[ \t]{0,3}(#{1,6})[ \t]+(.+?)\s*$")
    fence_pattern = re.compile(r"^[ \t]{0,3}```")
    in_fenced_code_block = False

    for line in markdown.splitlines():
        if fence_pattern.match(line):
            in_fenced_code_block = not in_fenced_code_block
            continue

        if in_fenced_code_block:
            continue

        match = header_pattern.match(line)
        if not match:
            continue

        level = len(match.group(1))
        text = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(2)).strip()
        headers.append((level, text))

    return headers
