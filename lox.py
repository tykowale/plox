#!/usr/local/bin/python3
from scanner import Scanner


def main():
    print("> Welcome to plox")
    run_prompt()


def run_prompt():
    while(True):
        run(input("> "))


def run(source: str):
    scanner = Scanner(source)
    print(source)


if __name__ == "__main__":
    main()
