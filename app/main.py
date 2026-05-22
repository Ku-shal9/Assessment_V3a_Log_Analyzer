import argparse
import sys

from parser import parsed_line
from report import generate_csv_report


def main():
    parser = argparse.ArgumentParser(description="Analyze a server log file")
    parser.add_argument(
        "log_file",
        nargs="?",
        default="../tests/sample.log",
        help="Path to the log file",
    )
    args = parser.parse_args()

    valid_lines = 0
    malformed_lines = 0
    logs = []

    try:
        with open(args.log_file, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                parsed = parsed_line(line)
                if parsed:
                    valid_lines += 1
                    logs.append(parsed)
                else:
                    malformed_lines += 1
    except FileNotFoundError:
        print(f"Error: file not found: {args.log_file}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        sys.exit(1)

    total = valid_lines + malformed_lines
    print(f"Lines read: {total}")
    print(f"Parsed: {valid_lines}")
    print(f"Skipped: {malformed_lines}")

    if not logs:
        print("No parseable lines — nothing to report.")
        return

    report_file = generate_csv_report(logs)
    print(f"\nCSV report generated: {report_file}")


if __name__ == "__main__":
    main()