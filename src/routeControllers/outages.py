from flask import Blueprint, jsonify, render_template, request
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.outagesFetcher import OutagesFetcher

# get application config
appConfig = getConfig()

outagesPage = Blueprint('outages', __name__,
                             template_folder='templates')


@outagesPage.route('/', methods=['GET', 'POST'])
def displayOutages():
    # in case of post request, fetch transmission elements outages and return json response
    if request.method == 'POST':
        startDateStr = request.form.get('startDate')
        endDateStr = request.form.get('endDate')
        outagesFetcher = OutagesFetcher(
            appConfig['outagesFetchUrl'])
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
        resp = outagesFetcher.fetchOutages(startDate, endDate)
        return render_template('displayOutages.html.j2', data=resp, startDate=startDateStr, endDate=endDateStr)
    # in case of get request just return the html template
    return render_template('displayOutages.html.j2')
