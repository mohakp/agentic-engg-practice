from markdown_utils import extract_headers


def test_extract_headers_returns_level_and_text_for_atx_headers():
    markdown = """# Title
Some intro.
## Section One
### Subsection
Not a header
"""

    assert extract_headers(markdown) == [
        (1, "Title"),
        (2, "Section One"),
        (3, "Subsection"),
    ]


def test_extract_headers_ignores_non_header_lines():
    markdown = """Text
- # Inside list item
Paragraph
"""

    assert extract_headers(markdown) == []


def test_extract_headers_strips_closing_hashes_and_whitespace():
    markdown = """##   Trim Me   ###
#### Keep This ####
"""

    assert extract_headers(markdown) == [
        (2, "Trim Me"),
        (4, "Keep This"),
    ]


def test_extract_headers_ignores_headers_inside_fenced_code_blocks():
    markdown = """# Real Header
```python
# Not a Header
## Also Not a Header
```
## Another Real Header
"""

    assert extract_headers(markdown) == [
        (1, "Real Header"),
        (2, "Another Real Header"),
    ]


def test_extract_headers_accepts_up_to_three_leading_spaces():
    markdown = """   # Indented Header
    # Too Indented
  ## Also Valid
"""

    assert extract_headers(markdown) == [
        (1, "Indented Header"),
        (2, "Also Valid"),
    ]
