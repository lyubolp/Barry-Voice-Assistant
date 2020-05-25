#!/usr/bin/python3
import pyjokes


def execute_action() -> str:
    return pyjokes.get_joke()


if __name__ == '__main__':
    print(execute_action())
