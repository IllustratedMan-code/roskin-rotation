import rich_click as click
from .select_control_studies import controlStudies


@click.group(help="a cool program")
def cli():
    pass


if __name__ == "__main__":
    cli()
