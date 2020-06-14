import asyncio

from . import update as updt
from . import score as scr

import aioredis
from aioredis.pubsub import Receiver
import traceback

import logging

async def score(ch, pub):
  """
  expected message structure:
  {
    "model":  #path to model to be used
    "data": #either json encoded data or base64 encoded json string
  }
  """
  logging.info("Started score subscription")
  while (await ch.wait_message()):
    try:  
      msg = await ch.get_json()
      logging.info("Got Message: {}".format(msg))

      if ("model" not in msg or
        "data" not in msg):
        raise Exception("Message corrupt", msg)

      score = scr.score(msg["model"], msg["data"])

      if score:
        pub.publish_json("ch:smartpass_score_result", score)

    except Exception as e:
      logging.error(f"Trace: {traceback.format_exc()}")

async def update(ch, pub):
  """
  expected message structure:
  {
    "data": #path to json file with data
    "target": #path where to put model
    "report": #path where to put report
  }
  """  
  logging.info("Started update subscription")
  while (await ch.wait_message()):
    try:  
      msg = await ch.get_json()
      
      logging.info("Got Message: {}".format(msg))
      logging.info(type(msg))
      
      if ("data" not in msg or
        "target" not in msg or
        "report" not in msg
      ):
        raise Exception("Message corrupt", msg)

      res = updt.update(msg["data"],
        msg["target"],
        msg["report"])
        
      if res:
        pub.publish_json("ch:smartpass_update_complete", {"complete": True})
    except Exception as e:
      logging.error(f"Trace: {traceback.format_exc()}")

async def main(host, port):
  pub = await aioredis.create_redis(
        'redis://{}:{}'.format(host, port))
  sub = await aioredis.create_redis(
        'redis://{}:{}'.format(host, port))

  subs = await sub.subscribe('ch:smartpass_score', 'ch:smartpass_update')

  task_score = asyncio.ensure_future(score(subs[0], pub))
  task_update = asyncio.ensure_future(update(subs[1], pub))

  await task_score
  await task_update
  sub.close()
  pub.close()
  