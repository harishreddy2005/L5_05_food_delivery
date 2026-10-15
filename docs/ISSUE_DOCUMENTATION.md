# Lab 5: Issue documentation

G Harish Reddy | PES1UG24AM366

Line numbers refer to the unchanged starter at commit `13d7380`.
Bandit severities are reported by the tool; the other categories describe impact,
not a severity score assigned by Pylint or Flake8.

| Issue | Type | Line number | Description | Fix approach | Tool that detected the issue |
|---|---|---|---|---|---|
| Unsafe deserialization (B301) | Security, medium | 49 | Loading a malicious pickle can execute arbitrary code. | Replace pickle with JSON; validate records before changing the queue. | Bandit |
| Pickle import (B403) | Security, low | 2 | The program depends on executable object serialization. | Remove pickle and use JSON for both backup and restore. | Bandit |
| Swallowed exceptions (B110/W0702/E722) | Security, low; error handling | 24-25 | A bare exception silently hides missing orders and unrelated errors. | Validate IDs and statuses and raise explicit ValueError; main displays rejected updates. | Bandit, Pylint, Flake8 |
| Shared mutable default (W0102) | Bug | 11 | The default history list survives between calls. | Use None; append only to an explicitly supplied history. | Pylint |
| Overly broad menu exception (W0718) | Error handling | 32 | Catching Exception hides programming errors. | Catch OSError and JSONDecodeError for expected file/parse failures. | Pylint |
| Unmanaged files (R1732) | Resource handling | 30, 43, 49 | Menu and restore files are not reliably closed; backup closing is manual. | Use with blocks for every file operation. | Pylint |
| Unspecified text encoding (W1514) | Portability | 30 | Menu decoding depends on the Windows default encoding. | Explicit UTF-8 for menu and JSON backups. | Pylint |
| Global rebinding (W0603) | Maintainability | 12, 28, 48 | Functions rebind shared state and the ID counter can collide after restore. | Update dictionaries in place and derive the next ID from existing IDs. | Pylint (global statements); collision identified by inspection |
| Missing documentation (C0114/C0116) | Maintainability | 1; 11, 21, 27, 35, 42, 47, 51, 56 | Module and functions lack descriptions. | Add concise module and function docstrings. | Pylint |
| Inconsistent names/string formatting (C0103/C0209) | Readability | 7, 51-52 | next_id is flagged as a constant; printQueue is not snake_case; old string interpolation is used. | Remove the separate counter, rename print_queue, use an f-string. | Pylint |
| Missing blank lines (E302/E305) | Style | 11, 21, 27, 35, 42, 47, 51, 56, 70 | Top-level definitions lack required separation. | Add two blank lines between top-level definitions and before the main guard. | Flake8 |
| Long lines (E501) | Style | 16, 54 | Lines exceed the default 79-character limit. | Expand the order record and keep queue printing within the limit. | Flake8 |

Additional actual defects found by running/reading the starter, not detected by
these tools: unknown sushi silently costs 99 (line 15); an empty customer/order
is accepted (line 60); teleported is accepted as a status (lines 23, 62); main
runs on import (line 70). These are fixed through validation and a main guard.
Tests also check item-list copying and fresh IDs after a JSON restore.

Commit overlap: the first commit replaces bare-except/pass as part of explicit
error handling, resolving B110 and E722 as well as Pylint W0702. The second removes
B301/B403 through JSON persistence. The third handles remaining formatting and
collects lab reports, documentation and regression tests. No warning suppressions
or relaxed tool settings are used.
