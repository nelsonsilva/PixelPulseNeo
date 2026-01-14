#!/usr/bin/env python
"""
Simple command runner for macOS testing.

Runs commands directly on the main thread, bypassing the scheduler.
This is required on macOS because PyGame/SDL needs the main thread for events.

Usage:
    python -m Matrix.driver.run arkanoid -d 60
    python -m Matrix.driver.run splash
    python -m Matrix.driver.run clock -d 30
"""
from dotenv import load_dotenv
load_dotenv()

import argparse
import threading
import importlib
import os


def list_commands() -> list[str]:
    """List available commands."""
    current_directory = os.path.dirname(os.path.realpath(__file__))
    commands = []
    for file in os.listdir(f"{current_directory}/commands"):
        if file.endswith("_cmd.py") and file != "base.py":
            command_name = file[:-7]  # Remove '_cmd.py'
            commands.append(command_name)
    return sorted(commands)


def run_command(command_name: str, duration: int = 30):
    """Run a single command directly on the main thread."""
    # Dynamically load the command class
    module_name = f"Matrix.driver.commands.{command_name}_cmd"
    class_name = f"{command_name.capitalize()}Cmd"

    try:
        module = importlib.import_module(module_name)
        command_class = getattr(module, class_name)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error: Could not load command '{command_name}'")
        print(f"  {e}")
        print(f"\nAvailable commands: {', '.join(list_commands())}")
        return

    # Instantiate and execute
    print(f"Running '{command_name}' for {duration} seconds...")
    cmd = command_class()
    stop_event = threading.Event()
    cmd.execute(stop_event, duration, [], {})
    print("Done.")


def main():
    parser = argparse.ArgumentParser(
        description="Test command runner for macOS (runs on main thread)"
    )
    parser.add_argument("command", nargs="?", help="Command name (e.g., arkanoid)")
    parser.add_argument(
        "-d", "--duration", type=int, default=30, help="Duration in seconds (default: 30)"
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available commands"
    )
    args = parser.parse_args()

    if args.list or not args.command:
        print("Available commands:")
        for cmd in list_commands():
            print(f"  {cmd}")
    else:
        run_command(args.command, args.duration)


if __name__ == "__main__":
    main()
