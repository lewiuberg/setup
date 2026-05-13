import argparse

from macsetup.app import MacsetupApp


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="macsetup",
        description="Wizard-driven macOS dev-environment setup.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview commands without running installs (file writes still happen).",
    )
    args = parser.parse_args()
    MacsetupApp(dry_run=args.dry_run).run()


if __name__ == "__main__":
    main()
