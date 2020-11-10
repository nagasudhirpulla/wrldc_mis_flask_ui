from flask import Blueprint, jsonify, render_template, request
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.longUnrevForcedOutagesFetcher import LongUnrevForcedOutagesFetcher

# get application config
appConfig = getConfig()

longUnrevForcedOutagesPage = Blueprint('longUnrevForcedOutages', __name__,
                                template_folder='templates')


@longUnrevForcedOutagesPage.route('/', methods=['GET', 'POST'])
def displayLongUnrevForcedOutages():
    # in case of post request, fetch displayLongUnrevForcedOutages and return json response
    if request.method == 'POST':
        startDateStr = request.form.get('startDate')
        endDateStr = request.form.get('endDate')
        longUnrevForcedOutagesFetcher = LongUnrevForcedOutagesFetcher(
            appConfig['longUnrevForcedOutagesFetchUrl'])
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
        resp = longUnrevForcedOutagesFetcher.fetchLongTimeUnrevForcedOutages(startDate, endDate)
        return render_template('displayLongUnrevForcedOutages.html.j2', data=resp, startDate=startDateStr, endDate=endDateStr)
    # in case of get request just return the html template
    return render_template('displayLongUnrevForcedOutages.html.j2')
