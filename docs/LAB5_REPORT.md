# Lab 5: Static Code Analysis

- Student: G Harish Reddy
- SRN: PES1UG24AM366
- University: PES University
- Lab: 5 - Static Code Analysis
- Date: 16 October 2026 (Asia/Calcutta)
- Repository: https://github.com/SETAPESU26/L5_05_food_delivery
- Assigned program: delivery_system.py
- Primary requirements: supplied Lab_5_Static_Code_Analysis_Student_handout.pdf

## Objective and tools

Improve the assigned Python program's quality, security and style by detecting,
documenting and fixing at least four actual issues with Pylint, Bandit and Flake8.
The local .venv uses Python 3.14.0, Pylint 4.1.3, Bandit 1.9.4 and Flake8 7.4.1.
pypdf 6.20.1 was used only to read the supplied handout.

## Issues and changes

See [ISSUE_DOCUMENTATION.md](ISSUE_DOCUMENTATION.md) (also supplied as [issues.md](issues.md), the README's requested
filename) for original line numbers, detector codes, descriptions and fixes.
Twelve issue categories are documented. The medium-severity unsafe pickle load
is removed. Both low-severity Bandit findings are resolved. Mutable defaults,
exception handling, resource management, documentation, naming and formatting
are corrected without suppression comments or relaxed configuration.

Validation additionally rejects unknown dishes, blank customers, empty orders,
unknown IDs and invalid delivery statuses. The demo retains examples of rejected
input, and also creates valid Asha and Ravi orders. Creating orders, updating
statuses, computing delivered revenue, printing the queue and saving/restoring
remain supported. Importing the module no longer runs the demo.

Backups now default to orders.json rather than orders.pkl. JSON object keys are
converted back to positive integer IDs. Invalid records and duplicate normalized
IDs are rejected before replacing live state. New orders after restore receive
an unused ID. Legacy pickle files are deliberately not loaded: retaining a pickle
reader would preserve the reported security vulnerability. Menu fallback behavior
for missing, unreadable or malformed JSON files is retained.

## Before and after

| Check | Before | After | Final exit code |
|---|---|---|---|
| Pylint | 6.27/10; 22 messages | 10.00/10; no messages | 0 |
| Bandit | 3 findings: medium 1, low 2, high 0 | 0 findings | 0 |
| Flake8 | 12 violations | 0 violations | 0 |

All tools analyzed delivery_system.py with their default checks. The six raw
reports are [pylint_before.txt](../reports/before/pylint_before.txt), [bandit_before.txt](../reports/before/bandit_before.txt), [flake8_before.txt](../reports/before/flake8_before.txt),
[pylint_after.txt](../reports/after/pylint_after.txt), [bandit_after.txt](../reports/after/bandit_after.txt) and [flake8_after.txt](../reports/after/flake8_after.txt). Empty [flake8_after.txt](../reports/after/flake8_after.txt) is
expected for a clean run. Before reports were created exclusively, before source
edits. Their SHA-256 hashes were checked unchanged after final analysis; hashes
and original exit codes are in [baseline_checksums.json](../reports/baseline_checksums.json). No baseline was overwritten.

## Runtime and tests

No existing tests were present in the starter. Added 12 unittest regression tests
for order totals/history/copying, separate calls, unknown dishes, empty input,
status validation, delivered-only revenue, menu loading/fallback, JSON round trips,
new IDs after restore, corrupt backups, invalid record fields, duplicate IDs and
queue output. Actual execution: 12 tests passed in 0.033 seconds, exit code 0.
Full names and output are in [test_results.txt](../evidence/test_results.txt).

The unchanged and final scripts were each run in a temporary working directory
to keep generated backups out of the repository. Both exited 0. Both reported
Revenue today: 290. Original output contains Ravi teleported 249 and a blank
customer with total 0. Final output explicitly rejects invalid inputs and contains
Asha delivered 290 and Ravi placed 150. See [program_before.txt](../evidence/program_before.txt) and [program_after.txt](../evidence/program_after.txt).
The source does not prompt for input, despite README.md mentioning a question.

## Reflection

The supplied PDF requests reflections but does not list specific questions.
README.md refers to four questions without their text. At the student's request,
[reflection.md](reflection.md) now provides a general reflection in four sections based on the
actual lab work: tool coverage, prioritization and fixes, limitations of static
analysis, and outcomes and future practice. These sections are not attributed to
the instructor as official questions.

## Three commits

| Commit | Message | Contents |
|---|---|---|
| afcfde4 | fix: resolve pylint code quality issues | Documentation, naming, resource handling, default argument, shared state, validation and import guard |
| 1964ac5 | fix: address bandit security findings | Remove pickle; use validated JSON backup/restore |
| 9e949fd | style: resolve flake8 violations | Remaining line lengths/blank lines; regression tests and complete available evidence/docs |

The first commit also resolves Bandit B110 and Flake8 E722 because their bare
exception overlaps Pylint's finding. The security commit resolves the remaining
Bandit findings. The formatting commit preserves the established behavior.
The three code-fix commits remain unchanged. A fourth documentation-only commit
completes the reflection and organizes the deliverables, so there are four new
commits in total. Use git log -4 --format="%h %s" to inspect them.
The student authorized pushing the completed repository to origin/main.

## Commands and reproduction

[COMMANDS.md](COMMANDS.md) records the PowerShell commands and capture procedure. The .venv
folder is ignored by the existing .gitignore. requirements-dev.txt pins the three
analysis tools. Tests use only Python's standard library.

## Verification status

Updated program, all six reports, issue table, runtime evidence, regression tests,
and the three requested commits are delivered. Final analysis meets all three
numeric/cleanliness targets. A general reflection is complete in [reflection.md](reflection.md);
the supplied materials contain no specific reflection questions. Clean static
analysis does not establish production readiness or validate every possible input.

The reflection, folder organization and documentation are included in the
separate documentation commit. Existing commit history has not been rewritten.
