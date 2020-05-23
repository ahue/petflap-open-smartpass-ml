# %%
import numpy as np
from datetime import datetime, time
import math

# %%
def scale(x, min_x, max_x,  a, b):
  return (b-a) * (x-min_x) / (max_x-min_x) + a

def densify_pattern(pattern, length):

  pat = pattern
  dense_pat = np.zeros(length)

  for i in range(0, len(pat)-1):
        tsl = pat[i]["ts"]
        tsr = pat[i+1]["ts"]

        xl = int(scale(tsl, pat[0]["ts"], pat[-1]["ts"], 0, length))
        xr = int(scale(tsr, pat[0]["ts"], pat[-1]["ts"], 0, length))

        if pat[i]["reading"] == 1:
          fill = 0
        else:
          if pat[i]["sensor"] == "out":
            fill = 1
          else: # sensor = in
            fill = 2

        print(xl)
        dense_pat[xl:xr] = fill
        
  return dense_pat.tolist()

# %%
def feat_daily(ts):
  if ts > 999999999:
    ts = int(ts / 1000)
  dt_obj = datetime.fromtimestamp(ts)


  utcnow = datetime.utcnow()
  midnight = datetime.combine(dt_obj.date(), time(0))
  delta = dt_obj - midnight
  print(delta.seconds)  # <-- careful
  feat = [math.sin(math.pi * delta.seconds / (24 * 60 * 60 / 2)),
    math.cos(math.pi * delta.seconds / (24 * 60 * 60 / 2))]
  return feat

# %%
