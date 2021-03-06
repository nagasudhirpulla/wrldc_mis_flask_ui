from flask import Blueprint, jsonify, render_template, request
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.iegcViolMsgsFetcher import IegcviolMsgsFetcher

# get application config
appConfig = getConfig()

iegcViolMsgsPage = Blueprint('iegcViolMsgs', __name__,
                              template_folder='templates')

@iegcViolMsgsPage.route('/', methods=['GET', 'POST'])
def displayIegcViolMsgs():
    # in case of post request, fetch iegc viol msgs and return json response
    if request.method == 'POST':
        startDateStr = request.form.get('startDate')
        endDateStr = request.form.get('endDate')
        iegcViolMsgsFetcher = IegcviolMsgsFetcher(
            appConfig['iegcViolMsgsFetchUrl'])
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
        resp = iegcViolMsgsFetcher.fetchIegcviolMsgs(startDate, endDate)
        msg= resp['data']
        return render_template('displayIegcViolMsgs.html.j2', data= msg, startDate=startDateStr, endDate=endDateStr)
    # in case of get request just return the html template
    return render_template('displayIegcViolMsgs.html.j2')