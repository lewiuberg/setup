import click

from macsetup import __version__
from macsetup.app import MacSetupApp


@click.command()
@click.version_option(__version__, prog_name="macsetup")
@click.option(
    "--wizard",
    is_flag=True,
    default=False,
    help="Force the first-run wizard, even if it's already been completed.",
)
@click.option(
    "--no-wizard",
    is_flag=True,
    default=False,
    help="Skip the first-run wizard and go straight to the dashboard.",
)
def main(wizard: bool, no_wizard: bool) -> None:
    """Interactive macOS setup tool."""
    if wizard and no_wizard:
        raise click.UsageError("--wizard and --no-wizard are mutually exclusive")
    app = MacSetupApp(force_wizard=wizard, force_dashboard=no_wizard)
    app.run()


if __name__ == "__main__":
    main()
