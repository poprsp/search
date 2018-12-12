#!/usr/bin/env python3

import sys

import search


def main() -> int:
    search.Dataset("data/wikipedia/Words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
