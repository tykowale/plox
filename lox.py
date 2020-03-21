#!/usr/local/bin/python3
import sys

from scanner import Scanner

had_error = False


def main() -> None:
    print("> Welcome to plox")
    run_prompt()


def run_prompt() -> None:
    while (True):
        run(input("> "))


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
