from flask import Blueprint, jsonify, render_template, request
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.majorGenOutagesFetcher import MajorGenOutagesFetcher

# get application config
appConfig = getConfig()

majorGenOutagesPage = Blueprint('majorGenOutages', __name__,
                                template_folder='templates')


@majorGenOutagesPage.route('/', methods=['GET', 'POST'])
def displayMajorGenOutages():
    # in case of post request, fetch major generating unit outages and return json response
    if request.method == 'POST':
        startDateStr = request.form.get('startDate')
        endDateStr = request.form.get('endDate')
        majorGenOutagesFetcher = MajorGenOutagesFetcher(
            appConfig['majorGenOutagesFetchUrl'])
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
        resp = majorGenOutagesFetcher.fetchMajorGenOutages(startDate, endDate)
        return render_template('displayMajorGenOutages.html.j2', data=resp, startDate=startDateStr, endDate=endDateStr)
    # in case of get request just return the html template
    return render_template('displayMajorGenOutages.html.j2')
