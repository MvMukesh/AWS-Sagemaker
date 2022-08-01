# -*- coding: utf-8 -*-
"""
Created on Mon Aug 1 10:30:40 2022

@author: Mukesh Manral
"""

import os
import json
import flask
import boto3
import time
import pyarrow
import pickle
import logging
import modin.pandas as pd
from sklearn.externals import joblib
from pyarrow import feather
from boto3.s3.connection import S3Connection
from botocore.exceptions import ClientError




#Define the path
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')
logging.info("Model Path" + str(model_path))

# Load the model components
regressor = joblib.load(os.path.join(model_path, 'model.pkl'))
logging.info("Regressor" + str(regressor))

# The flask app for serving predictions
app = flask.Flask(__name__)
@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    try:
        #regressor
        status = 200
        logging.info("Status : 200")
    except:
        status = 400
    return flask.Response(response= json.dumps(' '), status=status, mimetype='application/json' )

@app.route('/invocations', methods=['POST'])
def transformation():
    # Get input JSON data and convert it to a DF
    input_json = flask.request.get_json()
    input = input_json['input']['exp1']
    predictions = float(regressor.predict([[input]]))

    # Transform predictions to JSON
    result = {
        'output': predictions
        }

    resultjson = json.dumps(result)
    return flask.Response(response=resultjson, status=200, mimetype='application/json')
