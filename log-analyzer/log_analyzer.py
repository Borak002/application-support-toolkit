#!/usr/bin/env python3

"""
Application Support Toolkit
Log Analyzer

Analyzes application logs and summarizes common incident indicators.
"""

import re
import sys
from collections import Counter


PATTERNS = {
    "ERROR": re.compile(r"\bERROR\b", re.IGNORECASE),
    "EXCEPTION": re.compile(r"\bEXCEPTION\b", re.IGNORECASE),
    "TIMEOUT": re.compile(r"\bTIMEOUT\b|\bTIMED OUT\b", re.IGNORECASE),
    "HTTP 500": re.compile(r"\b500\b"),
    "HTTP 401": re.compile(r"\b401\b"),
    "HTTP 404": re.compile(r"\b404\b"),
    "HTTP 503": re.compile(r"\b503\b"),
}


def analyze_log(file_path):
    counts = Counter()
    total_lines = 0

    try:
        with open(file_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                total_lines += 1

                for category, pattern in PATTERNS.items():
                    if pattern.search(line):
                        counts[category] += 1

    except FileNotFoundError:
        print(f"Error: Log file not found: {file_path}")
        sys.exit(1)

    except PermissionError:
        print(f"Error: Permission denied: {file_path}")
        sys.exit(1)

    return total_lines, counts


def print_report(file_path, total_lines, counts):
    print("=" * 45)
    print("        APPLICATION LOG ANALYZER")
    print("=" * 45)
    print(f"Log file:       {file_path}")
    print(f"Total entries:  {total_lines}")
    print("-" * 45)

    for category, count in counts.items():
        print(f"{category:<15} {count}")

    print("-" * 45)

    total_issues = sum(counts.values())

    if total_issues == 0:
        print("STATUS: No common incident indicators found.")
    else:
        print(f"STATUS: {total_issues} incident indicators detected.")

    print("=" * 45)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 log_analyzer.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    total_lines, counts = analyze_log(log_file)
    print_report(log_file, total_lines, counts)


if __name__ == "__main__":
    main()
