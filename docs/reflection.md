# Lab 5: Reflection

**Name:** G Harish Reddy
**SRN:** PES1UG24AM366
**Lab:** 5 - Static Code Analysis

The supplied handout requests a reflection but does not list specific questions.
The following four sections reflect on the completed analysis and fixes; they
are not presented as instructor-provided questions.

## Role of the three tools

This lab demonstrates how the tools complement each other. Pylint identified
quality and maintainability problems, including a mutable default argument,
broad exception handling, missing documentation and unmanaged files. Bandit
identified unsafe pickle deserialization and silently swallowed exceptions.
Flake8 identified formatting problems such as missing blank lines, long lines
and a bare except. Using all three provided wider coverage than using only one.

## Prioritizing and fixing findings

The most significant security finding was the medium-severity pickle.load call.
A malicious pickle can execute code when loaded. Replacing pickle with JSON
removed executable deserialization, while validating restored records prevented
invalid data from replacing the live queue. This changes the backup format to
orders.json; existing pickle backups are not loaded.

Other fixes improved correctness and clarity. Replacing the shared default
history list with None avoided retaining hidden state across calls. Explicit
validation and errors replaced silent exception handling. Context managers
ensured files close reliably, and UTF-8 made text handling explicit. These
changes addressed the underlying causes rather than suppressing warnings.

## What static analysis missed

Running and reading the original program revealed business-rule defects that
the tools did not report: an unknown dish silently cost 99, an empty customer
and order were accepted, and teleported was accepted as a delivery status.
These examples show that a clean analysis report cannot establish functional
correctness. Domain rules still need review and execution-based tests.

Twelve regression tests checked order totals, rejected inputs, valid status
updates, delivered-only revenue, menu fallback, backup round trips and invalid
backup handling. The final demo still reported revenue of 290 while explicitly
rejecting invalid input. Combining these checks with static analysis provided
stronger evidence that the program continued to perform its intended tasks.

## Outcome and future practice

The Pylint score improved from 6.27/10 to 10.00/10. Bandit's three findings were
resolved, and Flake8's twelve violations were eliminated. All twelve regression
tests passed. These results show improvements in the issues checked by the tools;
they do not prove that every possible defect has been removed.

For future projects, a useful workflow is to save a baseline, prioritize security
and correctness problems, make focused changes, and rerun analysis alongside
behavioral tests. Running these checks before committing or in continuous
integration can help catch regressions early. Readable code, explicit validation
and documented behavior also make later maintenance easier.
