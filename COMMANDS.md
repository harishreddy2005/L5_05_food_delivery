# Commands executed and reproduction

Working folder: `C:\L5_05_food_delivery`. Commands use Windows PowerShell.

The repository was cloned using:

```powershell
git clone https://github.com/SETAPESU26/L5_05_food_delivery.git C:\L5_05_food_delivery
Set-Location C:\L5_05_food_delivery
```

Inspection included Get-Content README.md, delivery_system.py and .gitignore;
rg --files; git status --short; git log; and Python/Git version checks.

Setup commands executed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pylint bandit flake8 pypdf
```

The handout was extracted with pypdf.PdfReader through Python with -X utf8.
No environment activation is needed when using the explicit interpreter path.
To reproduce the tool versions, install -r requirements-dev.txt instead.

Analysis was executed by a Python subprocess wrapper launched from PowerShell.
It invoked these exact tool argument sequences before edits and again after fixes:

```powershell
.\.venv\Scripts\python.exe -m pylint delivery_system.py
.\.venv\Scripts\python.exe -m bandit -r delivery_system.py
.\.venv\Scripts\python.exe -m flake8 delivery_system.py
```

The wrapper captured stdout and stderr together, recorded exit codes, and wrote
UTF-8 text to each tool's *_before.txt or *_after.txt. Baselines were opened in
exclusive creation mode (`open('x')`), and hashes were verified after the final
run. To rerun interactively, use the commands above; do not redirect over the
baseline files. Pylint and Bandit were also run between the fix commits.

Verification command executed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

Output was captured into test_results.txt. The wrapper also ran the absolute
path to delivery_system.py with subprocess.run in a TemporaryDirectory before
and after edits, saving program_before.txt and program_after.txt. This keeps
orders.pkl/orders.json artifacts outside the checkout. To run the final demo
manually from the repository:

```powershell
.\.venv\Scripts\python.exe delivery_system.py
```

That command creates orders.json in the current working directory.

The following commits were created with git add of the corresponding files and:

```powershell
git commit -m "fix: resolve pylint code quality issues"
git commit -m "fix: address bandit security findings"
git commit -m "style: resolve flake8 violations"
```

Final verification uses git diff --check, git status --short,
git log -3 --format="%h %s", and git rev-list --count 13d7380..HEAD.
No push command was executed.
