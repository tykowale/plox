#!/usr/local/bin/python3
import sys


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str) -> None:
    print(f"[{line}] Error {where}: {message}", file=sys.stderr)
