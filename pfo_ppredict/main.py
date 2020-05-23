import click
from . import update as updt
from . import score as scr
import json
import sys

@click.group()
def cli():
  pass

@cli.command()
@click.option("-i", "--input", "data", help="training data")
@click.option("-t", "--target", help="where to write the model")
@click.option("-r", "--report", help="where to write the target")
def update(data, target, report):
    """Update the model"""
    updt.update(data, target, report)
    sys.exit(0)

@cli.command()
@click.option("-m", "--model", required=True, help="The pickled model pipeline to use.")
@click.option("-d","--data", required=True, help="The data to score.")
def score(model, data):
    """Use the model."""
    scores = scr.score(model, data)
    print(json.dumps(scores))
    sys.exit(0)

if __name__ == '__main__':
    cli()