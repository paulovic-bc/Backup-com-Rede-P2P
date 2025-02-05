import argparse
import platform
from os import system
from pathlib import Path
from sys import exit

from dotenv import load_dotenv

load_dotenv("./src/.env")

# Base directory for the project, determined by the script's location
BASE_DIR = Path(__file__).resolve().parent


def run_command(command: str) -> int:
    """
    Runs a system command and returns the status code.

    Args:
        command (str): The command to run.

    Returns:
        int: The exit status of the command (0 for success, non-zero for failure).
    """
    print(f"\nRunning command: {command}")
    return system(command)


def create_fixtures() -> None:
    """
    Loads predefined fixtures into the database by running the 'loaddata' Django command
    for a list of fixtures.
    """
    fixtures = ["nodes"]

    app_data_command = f'python "{path}" loaddata '
    for fixture in fixtures:
        app_data_command += f"{fixture} "

    run_command(app_data_command)


def start_server(port: int) -> None:
    """
    Starts the server in standard HTTP mode.
    """
    run_server = f'python "{path}" runserver 0.0.0.0:{port}'

    if run_command(run_server) != 0:
        exit(1)


def main() -> None:
    """
    Main entry point of the script. Handles database migrations, testing, and
    starting the server based on the command-line arguments.
    """
    migrations_command = f'python "{path}" makemigrations && python "{path}" migrate'
    if run_command(migrations_command) != 0:
        exit(1)

    if args.tests:
        test_command = f'python "{path}" test --parallel --noinput'

        if run_command(test_command) != 0:
            exit(1)

    create_fixtures()

    start_server(args.port)


if __name__ == "__main__":
    path = f"{BASE_DIR}/manage.py"

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--tests", help="Run tests", dest="tests", action="store_true"
    )

    parser.add_argument(
        "-p",
        "--port",
        help="Port to run the server",
        type=int,
        default=8001,
    )

    args = parser.parse_args()

    try:
        main()
    except:
        exit(0)
