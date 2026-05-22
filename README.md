# Log Analyzer

## Prerequisites

- Python 3.8+
- pip
- pandas

```bash
pip install pandas
```

## Run

From the project root:

```bash
cd app
python3 main.py /path/to/your.log
```

Default (uses `tests/sample.log` if you omit the path):

```bash
python3 main.py
```

Output: `app/log_report.csv`
