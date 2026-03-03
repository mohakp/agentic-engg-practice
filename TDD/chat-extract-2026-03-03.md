# Chat Extract - 2026-03-03

## Session Highlights

- Initialized a Git repository in the workspace.
- Created the `TDD` folder.
- Implemented `extract_headers(markdown: str)` in `TDD/markdown_utils.py` using red/green TDD.
- Added and ran tests in `TDD/test_markdown_utils.py`.
- Completed two TDD cycles:
  - Initial feature tests (ATX headers, ignores non-headers, trims trailing hashes).
  - Edge-case tests (ignore fenced code blocks, allow up to 3 leading spaces).
- Verified the test suite passes: `5 passed`.

## Current State

- Core files:
  - `TDD/markdown_utils.py`
  - `TDD/test_markdown_utils.py`
- Test command:
  - `python -m pytest -q`

## Actual Prompts

1. `first do git init. then create a folder called TDD.`
2. `change to TDD folder and perform the following task:
Build a Python function to extract headers from a markdown string. Use red/green TDD.`
3. `yes`
4. `run the test suit again`
5. `first create a .md file with an extract of this chat, in TDD with appended current date. then push it to https://github.com/mohakp/agentic-engg-practice.git`
6. `add actual prompts in .md file`
7. `yes push it`
8. `add all prompts in this chat to .md`

---

Generated on: 2026-03-03
