#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 23:15:09 2017

@author: gjacopo
"""

from __future__ import print_function

import requests

import pandas as pd
import numpy as np#analysis:ignore
from matplotlib import pyplot as plt

from fbprophet import Prophet
    
PROTOCOL        = "http"
API_LANG        = "en"
API_FMT         = "json"
API_DOMAIN      = 'ec.europa.eu/eurostat/wdds'
API_VERS        = 2.1
API_URL         = "{}://{}/rest/data/v{}/{}/{}".format(
                  PROTOCOL, API_DOMAIN, API_VERS, API_FMT, API_LANG
                  )

def build_url(indicator, **kwargs):
    url = "{}/{}?".format(API_URL, indicator[0])
    if 'geo' in kwargs:
        url = "{}geo={}&".format(url, kwargs.pop('geo', None))
    if 'time' in kwargs:
        url = "{}time={}&".format(url, kwargs.pop('time', None))
    #_izip_replicate = lambda d : [[(k,i) for i in d[k]] if isinstance(d[k], (tuple,list))        \
    #        else (k, d[k])  for k in d]    
    _no_replicate = lambda d : d.items()
    filters = '&'.join(['{k}={v}'.format(k=k, v=v[0]) for (k, v) in _no_replicate(kwargs)])
    url = "{}{}".format(url, filters)
    return url
    
def get_response(url):
    # request the URL
    session = requests.session()
    try:
        response = session.head(url)
        response.raise_for_status()
    except:
        raise IOError("ERROR: wrong request formulated")  
    else:
        print ("OK: status={}".format(response.status_code))
    
    # load the data
    try:    
        response = session.get(url)
    except:
        raise IOError('error retrieveing response from URL')    
    
    if API_FMT == 'json':
        resp = response.json()
    elif API_FMT == 'unicode':
        resp = response.text
       
    return resp
    
def build_dataframe(resp):
    lbl2idx = resp['dimension']['time']['category']['index']
    idx2lbl = {v:k for (k,v) in lbl2idx.items()}
    data = resp['value']
    data = {idx2lbl[int(k)]:v for (k,v) in data.items()}
    try:
        assert None # not needed, and also because it adds a day date
        from datetime import datetime
        table = {datetime.strptime(k.replace('M','-'), '%Y-%m'): v      \
                 for (k,v) in data.items()}
        # instead we will use pandas.datetime below
    except:
        table = {k.replace('M','-'):v for (k,v) in data.items()}    
    # create data frame with columns ds (date type) and y, the time series.
    df = pd.DataFrame(list(table.items()), columns=['ds','y'])
    # df = df[df['y'].notnull()]
    df.sort_values('ds', inplace=True)    
    ds_last = df['ds'].values[-1]
    df['ds'] = pd.to_datetime(df['ds'])
    return df, ds_last

def predict_prophet(df, nyears):
    # we fit the model by instantiated a new Prophet object.
    m = Prophet(growth = "linear", yearly_seasonality=True, weekly_seasonality=False)
    # we call its fit method and pass in the historical dataframe
    m.fit(df)    
    # we extend into the future a specified number of days
    future = m.make_future_dataframe(periods=12*nyears, freq='M')
    fcst = m.predict(future)
    return m, fcst

def plot_historical(df, ylabel="", last=""):
    xlabel = "Time"
    fig = plt.figure(facecolor='w', figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(df['ds'], df['y'], 'k.')
    ax.plot(df['ds'], df['y'], ls='-', c='#0072B2')
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.set_xlabel(xlabel, fontsize=14); 
    ax.set_ylabel(ylabel, fontsize=14)
    fig.suptitle("Historical data (last: {})".format(last), fontsize=16)
    fig.tight_layout()
    
def plot_predict(m, fcst, ylabel="", period="", last=""):
    xlabel = "Time"
    fig = m.plot(fcst, uncertainty=True) 
    plt.axvline(pd.to_datetime(last), color='r', linestyle='--', lw=2)
    plt.xlabel(xlabel, fontsize=14); 
    plt.ylabel(ylabel, fontsize=14)
    fig.suptitle("Forecast data ({} years)".format(period), fontsize=16)
    # fig.savefig('tour_occ_nim_predict.png')  
    fig = m.plot_components(fcst, uncertainty=True);
    fig.suptitle("Forecast components", fontsize=16)

def run_forecast(indicator, geo, filters, period, label="indic_to"):
    # input data loading and formatting
    url = build_url(indicator, geo=geo, **filters)  
    resp = get_response(url)
    df, ds_last = build_dataframe(resp)  
    df.head(); df.tail()
    ylabel = "{} : {} - {}".format(indicator[0], filters[label][1], geo)  
    plot_historical(df, ylabel=ylabel, last=ds_last)
    
    # forecast configuration and estimation    
    m, fcst = predict_prophet(df, period)
    # fcst[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    plot_predict(m, fcst, ylabel=ylabel, period=period, last=ds_last)

GEO             = "EU28"
# TIME          = all
NYEARS          = 1

## run tour_occ_nim estimation    
indicator       = (u'tour_occ_nim', "Tour accomodation")
## http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tour_occ_nim&lang=en
filters       = {'unit': (u'NR', "Number of nights"),
                'nace_r2': (u'I551', "Hotels; holiday and other short-stay accommodation..."),
                'indic_to': (u'B006', "Nights spent, total")
                }             
run_forecast(indicator, GEO, filters, NYEARS)

## run une_rt_m estimation    
indicator       = (u'une_rt_m', "Unemployment")
# http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=une_rt_m&unit=THS_PER&age=TOTAL&sex=T&s_adj=NSA
filters       = {'unit': (u'THS_PER', "Population count"),
                'age': (u'TOTAL', "Age"),
                'sex': (u'T', "Sex"),
                # 's_adj': (u'SA', "Seasonally adjusted data")
                's_adj': (u'NSA', "Unadjusted data")
                }             
run_forecast(indicator, GEO, filters, NYEARS, label='s_adj')


