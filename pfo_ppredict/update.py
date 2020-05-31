
# %%
import json
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

# from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline

from . import utils as utl

import pickle as pkl
import os
# import codecs

# %%

def update(src, target, report_target):

  data = load_data(src)

  df = create_df(data)

  result = build_model(df[0], df[1])

  store_model(result[0], target)

  store_report(result[1], report_target)

  pass


# %%

def load_data(src):
  with open(src, 'r') as data:
    passages = json.load(data)
    return passages

# %%
def create_df(passages):

  y = [
    p["direction"]["set"] if "set" in p["direction"] else p["direction"]["predicted"]
  for p in passages]

  X = passages
  # pd.DataFrame([ utl.densify_pattern(p["pattern"], 600) +
  # [p["duration"]] + utl.feat_daily(p["start"])
  #  for p in passages])

  return (X, y)

# %%
def build_model(X, y):

  X_train, X_test, y_train, y_test = train_test_split(X, y)
  
  pipln = make_pipeline(
                    utl.PassagePreprocessor(600),
                    StandardScaler(),
                     MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)
                     )
  
  pipln.fit(X_train, y_train)
  
  pipln.predict(X_test)

  predictions = pipln.predict(X_test)

  report = classification_report(y_test, predictions, output_dict=True)
  
  return (pipln, report)

# %%
def store_model(mdl, target):
  os.makedirs(os.path.dirname(target), exist_ok=True)
  with open(target, "wb") as f:
    pkl.dump(mdl, f)
  
# %%
def store_report(report, target):
  os.makedirs(os.path.dirname(target), exist_ok=True)
  with open(target, "w") as f:
    json.dump(report, f)