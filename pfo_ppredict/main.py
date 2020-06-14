import click
from . import update as updt
from . import score as scr
from . import redis_subscriber as sub
import json
import sys
import asyncio
import traceback
import os

import logging

log_dir = "/var/log/pfo/smartpass"
log_file = log_dir + "/model_server.log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO, filename=log_file)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

@click.group()
def cli():
  pass

@cli.command()
@click.option("-i", "--input", "data", help="Path to training data")
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
    logging.info(json.dumps(scores))
    sys.exit(0)

@cli.command()
@click.option("-h", "--host", required=True, help="host of the redis instance")
@click.option("-p", "--port", required=True, help="port of redis instance")
@click.option("-k", "--kill", required=False, default=True, help="Kill existing process, if not set, start will fail if process is already running")

def run(host, port, kill):
    """Run a service that listens to redis channels."""
    
    import signal

    pid_dir = "/tmp/pfo/smartpass"
    pid_file = pid_dir + "/model_server.pid"
    if not os.path.exists(pid_dir):
        os.makedirs(pid_dir, exist_ok=True)
    if os.path.isfile(pid_file):
        with open(pid_file, "r") as f:
            pid = f.readline()


        if kill:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except Exception:
                logging.warn(f"Trace: {traceback.format_exc()}")
                logging.warn("Could not kill PID {}".format(pid))
        else:
            raise Exception("Already instance running with PID {}".format(pid))
            
    
    pid = os.getpid()
    with open(pid_file, "w+") as f:
        f.write(str(pid))
    
    try:
        asyncio.run(sub.main(host, port))
    except (Exception, KeyboardInterrupt) as e:
        logging.error(f"Trace: {traceback.format_exc()}")
        os.remove(pid_file)
        raise e
        
    
    os.remove(pid_file)
    sys.exit(0)

if __name__ == '__main__':
    cli()