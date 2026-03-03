# Markdown Header Extractor Walkthrough

*2026-03-03T14:18:07Z by Showboat 0.6.1*
<!-- showboat-id: 7442e0e2-9591-4ac1-968d-de90f8607434 -->

This document is a linear walkthrough of the markdown header extractor implementation.

Plan of walkthrough:
1. Start from repository context and file responsibilities.
2. Walk top-to-bottom through `TDD/markdown_utils.py` and explain each decision.
3. Walk top-to-bottom through `TDD/test_markdown_utils.py` and map each test to behavior.
4. Conclude with a quick execution path: what happens from input markdown to output tuples.

Repository context: this mini project has one implementation module and one test module inside the TDD folder.

```powershell
Get-ChildItem TDD | Select-Object Name,Length
```

```output

Name                       Length
----                       ------
.pytest_cache                    
__pycache__                      
chat-extract-2026-03-03.md 877   
markdown_utils.py          830   
test_markdown_utils.py     1315  


```

Linear walkthrough begins with TDD/markdown_utils.py. We will inspect the file in execution order and explain each branch.

```python
from pathlib import Path; lines=Path('TDD/markdown_utils.py').read_text().splitlines(); [print(f'{i+1}: {lines[i]}') for i in range(0,10)]
```

```output
1: import re
2: 
3: 
4: def extract_headers(markdown: str) -> list[tuple[int, str]]:
5:     """Extract ATX-style markdown headers as (level, text) tuples."""
6:     headers: list[tuple[int, str]] = []
7:     header_pattern = re.compile(r"^[ \t]{0,3}(#{1,6})[ \t]+(.+?)\s*$")
8:     fence_pattern = re.compile(r"^[ \t]{0,3}```")
9:     in_fenced_code_block = False
10: 
```

Step 1 (setup):
- `re` is imported for regex matching and cleanup.
- `extract_headers` receives one markdown string and returns a list of `(level, text)` tuples.
- `headers` is the accumulator.
- `header_pattern` recognizes ATX headers with:
  - optional indentation (0-3 spaces/tabs),
  - 1 to 6 leading `#`,
  - required whitespace after marker,
  - captured header text.
- `fence_pattern` detects triple-backtick fences (also allowing up to 3 leading spaces).
- `in_fenced_code_block` tracks whether parsing is currently inside a fenced region.

```python
from pathlib import Path; lines=Path('TDD/markdown_utils.py').read_text().splitlines(); [print(f'{i+1}: {lines[i]}') for i in range(10,len(lines))]
```

```output
11:     for line in markdown.splitlines():
12:         if fence_pattern.match(line):
13:             in_fenced_code_block = not in_fenced_code_block
14:             continue
15: 
16:         if in_fenced_code_block:
17:             continue
18: 
19:         match = header_pattern.match(line)
20:         if not match:
21:             continue
22: 
23:         level = len(match.group(1))
24:         text = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(2)).strip()
25:         headers.append((level, text))
26: 
27:     return headers
```

Step 2 (line-by-line parsing):
- The parser scans each line in order using `splitlines()`.
- When a fence line is seen, the boolean flips; that makes matching symmetric for opening/closing fences.
- Immediately after a fence toggle, the line is skipped (`continue`) so a fence line is never treated as a header.
- While `in_fenced_code_block` is true, all lines are ignored.
- Outside fenced blocks, each line is tested with `header_pattern`.
- If matched:
  - `level` is count of leading `#` characters,
  - `text` removes optional trailing closing hashes (e.g. `### Title ###` -> `Title`) and trims whitespace,
  - tuple is appended to `headers`.
- Finally, the collected tuples are returned in original document order.

Next, we walk through TDD/test_markdown_utils.py top-to-bottom. Each test documents one functional requirement or edge case.

```python
from pathlib import Path; lines=Path('TDD/test_markdown_utils.py').read_text().splitlines(); [print(f'{i+1}: {lines[i]}') for i in range(0,37)]
```

```output
1: from markdown_utils import extract_headers
2: 
3: 
4: def test_extract_headers_returns_level_and_text_for_atx_headers():
5:     markdown = """# Title
6: Some intro.
7: ## Section One
8: ### Subsection
9: Not a header
10: """
11: 
12:     assert extract_headers(markdown) == [
13:         (1, "Title"),
14:         (2, "Section One"),
15:         (3, "Subsection"),
16:     ]
17: 
18: 
19: def test_extract_headers_ignores_non_header_lines():
20:     markdown = """Text
21: - # Inside list item
22: Paragraph
23: """
24: 
25:     assert extract_headers(markdown) == []
26: 
27: 
28: def test_extract_headers_strips_closing_hashes_and_whitespace():
29:     markdown = """##   Trim Me   ###
30: #### Keep This ####
31: """
32: 
33:     assert extract_headers(markdown) == [
34:         (2, "Trim Me"),
35:         (4, "Keep This"),
36:     ]
37: 
```

Tests section A:
- Test 1 validates the primary contract: detect ATX headers and return exact `(level, text)` tuples.
- Test 2 ensures normal text and list-item content like `- # ...` are not false positives.
- Test 3 validates cleanup behavior for trailing closing hashes and surrounding whitespace.

These three tests define the base behavior before edge conditions.

```python
from pathlib import Path; lines=Path('TDD/test_markdown_utils.py').read_text().splitlines(); [print(f'{i+1}: {lines[i]}') for i in range(37,len(lines))]
```

```output
38: 
39: def test_extract_headers_ignores_headers_inside_fenced_code_blocks():
40:     markdown = """# Real Header
41: ```python
42: # Not a Header
43: ## Also Not a Header
44: ```
45: ## Another Real Header
46: """
47: 
48:     assert extract_headers(markdown) == [
49:         (1, "Real Header"),
50:         (2, "Another Real Header"),
51:     ]
52: 
53: 
54: def test_extract_headers_accepts_up_to_three_leading_spaces():
55:     markdown = """   # Indented Header
56:     # Too Indented
57:   ## Also Valid
58: """
59: 
60:     assert extract_headers(markdown) == [
61:         (1, "Indented Header"),
62:         (2, "Also Valid"),
63:     ]
```

Tests section B:
- Test 4 validates fenced-code handling. Headers inside triple-backtick blocks must be ignored, while headers before/after the block still count.
- Test 5 validates indentation policy from CommonMark-style rules: up to three leading spaces are allowed; four spaces should not be recognized as a header.

Together, these tests justify both regex choices (`{0,3}` and fence detection) and the state machine (`in_fenced_code_block`).

Execution path summary: given markdown input, the function scans each line once, toggles fenced-state on backticks, matches headers only when outside fences, normalizes header text, and returns ordered tuples.

```python
from TDD.markdown_utils import extract_headers; fence=chr(96)*3; sample='\n'.join(['# A', f'{fence}py', '## B', fence, '### C ###']); print(extract_headers(sample))
```

```output
[(1, 'A'), (3, 'C')]
```
