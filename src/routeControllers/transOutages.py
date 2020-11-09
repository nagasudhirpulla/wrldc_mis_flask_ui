from flask import Blueprint, jsonify, render_template, request
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.transOutagesFetcher import TransOutagesFetcher

# get application config
appConfig = getConfig()

transOutagesPage = Blueprint('transOutages', __name__,
                             template_folder='templates')


@transOutagesPage.route('/', methods=['GET', 'POST'])
def displayTransOutages():
    # in case of post request, fetch transmission elements outages and return json response
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        transOutagesFetcher = TransOutagesFetcher(
            appConfig['transOutagesFetchUrl'])
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        resp = transOutagesFetcher.fetchTransOutages(startDate, endDate)
        return render_template('displayTransOutages.html.j2', data=resp)
    # in case of get request just return the html template
    return render_template('displayTransOutages.html.j2')
