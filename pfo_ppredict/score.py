
import pickle as pkl
import json
import base64

def load_model(src):

  with open(src, "rb") as f:
    mdl = pkl.load(f)
    return mdl

def parse_data(data):

  decoded = base64.b64decode(data)  

  return json.loads(decoded)

def score(model, data):
  
  mdl = load_model(model)

  if type(data) is not dict:
    data = parse_data(data)

  if type(data) != list:
    X = [data]
  else:
    X = data

  pred = mdl.predict(X)
  proba = mdl.predict_proba(X)
  
  return [{"_id": X[i]["_id"],"pred": pred[i], "proba": max(proba[i]) } for i in range(len(X))]