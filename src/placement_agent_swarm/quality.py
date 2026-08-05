import subprocess
import sys


def run_command(command: list[str]) -> int:
    result = subprocess.run(command, check=False)
    return result.returncode


def main() -> None:
    commands = [
        ["ruff", "check", "."],
        ["mypy", "src"],
        ["pytest", "-v"],
    ]

    for command in commands:
        exit_code = run_command(command)

        if exit_code != 0:
            sys.exit(exit_code)

    print("All quality checks passed.")


if __name__ == "__main__":
    main()