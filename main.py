#!/usr/bin/env python3
"""Endless Winter - Post-apocalyptic 2D survival game entry point."""

from game.engine import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
