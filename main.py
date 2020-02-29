# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 23:01:52 2019

@author: waels
"""

from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, escape, request
from review_analysis import *
from elastic import *
import pandas as pd
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def read_preprocess_data(path):
    df = pd.read_csv(path)
    df = df.loc[df['categories'] == 'Hotels']
    df.drop(columns=['reviews.doRecommend', 'reviews.id'])
    float_cols = df.select_dtypes(include=['float64']).columns
    str_cols = df.select_dtypes(include=['object']).columns
    df.loc[:, float_cols] = df.loc[:, float_cols].fillna(0)
    df.loc[:, str_cols] = df.loc[:, str_cols].fillna('')    
    df['reviews.date'] = pd.to_datetime(df['reviews.date'])
    df['reviews.date'].fillna(df['reviews.date'].mean(), inplace=True)
    return df
    

data_path = r'data\7282_1.csv'
df = read_preprocess_data(data_path)
    
authenticator = IAMAuthenticator('rmfIql5Of4jHxHG3mCOpRBZ9dKGI7KS5cahwQifC2rcB')
tone_analyzer = ToneAnalyzerV3(
   version='2017-09-21',
   authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/3365d25b-affc-47c2-bed6-b6e8a1c3687c')


app = Flask(__name__)

# create elasticsearch object & index
es, index_name = create_es()

@app.route('/tone/<string:hotel_name>')
def tone(hotel_name):
    return get_hotel_tones(hotel_name, df, tone_analyzer)

@app.route('/index_hotels')
def index_hotels():
    index_hotels_es(df, es, index_name, tone_analyzer)
    return 'indexing done'

@app.route('/get_hotel/<string:hotel_name>')
def get_hotel(hotel_name):
    return get_hotel_es(hotel_name, es, index_name)
    
if __name__ == "__main__":
    app.run(debug=True)
    
    