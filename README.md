# Lab 5: Static Code Analysis — Food Delivery Order Queue Manager

## Completed lab files

Start with the [Lab 5 report](docs/LAB5_REPORT.md),
[issue table](docs/ISSUE_DOCUMENTATION.md),
[reflection](docs/reflection.md), and [commands](docs/COMMANDS.md).
The original assignment instructions are preserved below.

```text
L5_05_food_delivery/
|-- delivery_system.py
|-- test_delivery_system.py
|-- requirements-dev.txt
|-- README.md
|-- docs/
|   |-- LAB5_REPORT.md
|   |-- ISSUE_DOCUMENTATION.md
|   |-- issues.md
|   |-- reflection.md
|   `-- COMMANDS.md
|-- reports/
|   |-- baseline_checksums.json
|   |-- before/
|   |   |-- pylint_before.txt
|   |   |-- bandit_before.txt
|   |   `-- flake8_before.txt
|   `-- after/
|       |-- pylint_after.txt
|       |-- bandit_after.txt
|       `-- flake8_after.txt
`-- evidence/
    |-- program_before.txt
    |-- program_after.txt
    `-- test_results.txt
```

`.gitignore`, `.git/`, `.venv/`, and `__pycache__/` are also present;
the environment and Python cache are ignored by Git.

**Your file:** `delivery_system.py`

Follow the lab handout for the full instructions.

## About the program

An order queue for a food delivery kitchen. It creates orders from a menu, moves them through delivery statuses, totals the day's revenue and backs the queue up to disk.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:
   ```bash
   python delivery_system.py
   ```
   It asks one question. Press Enter to use the default, then try a few inputs of your own. Not every problem in this file is something a tool will flag, so pay attention to output that looks wrong.

2. **Install the tools:**
   ```bash
   pip install pylint bandit flake8
   ```

3. **Run the analysis** and save the reports:
   ```bash
   pylint delivery_system.py > pylint_report.txt
   bandit -r delivery_system.py > bandit_report.txt
   flake8 delivery_system.py > flake8_report.txt
   ```

4. **Document the issues** in [issues.md](docs/issues.md) using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ... | ... | ... | ... | ... |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in [reflection.md](docs/reflection.md).

## Deliverables

1. `delivery_system.py`: your cleaned version, with at least 4 issues fixed.
2. [issues.md](docs/issues.md): the completed issue table.
3. [reflection.md](docs/reflection.md): your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
