from flask import Blueprint, jsonify, render_template, request
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.derFreqFetcher import DerivedFrequencyFetcher


# get application config
appConfig = getConfig()

derviedFreqPage = Blueprint('derivedFreq', __name__,
                              template_folder='templates')


@derviedFreqPage.route('/', methods=['GET', 'POST'])
def displayDerivedFrequency():
    if request.method == 'POST':
        startDateStr= request.form.get('startDate')
        endDateStr= request.form.get('endDate')
        derFreqFether = DerivedFrequencyFetcher(appConfig['derivedFrequencyFetchUrl'])
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
        resp = derFreqFether.fetchDerivedFrequency(startDate, endDate)
        return render_template('displayDerivedFreq.html.j2',data=resp, method=request.method, startDate=startDateStr, endDate=endDateStr)
    # in case of get request just return the html template
    return render_template('displayDerivedFreq.html.j2', method=request.method)
