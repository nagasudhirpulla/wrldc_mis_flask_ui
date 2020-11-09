from flask import Blueprint, jsonify, render_template, request, abort, send_file
import datetime as dt
import os
from src.appConfig import getConfig
from src.services.weeklyReportCreationHandler import WeeklyReportCreationHandler
from src.utils.stringUtils import getReadableByteSize, getTimeStampString


# get application config
appConfig = getConfig()

weeklyReportsPage = Blueprint('weeklyReport', __name__,
                              template_folder='templates')


@weeklyReportsPage.route('/create', methods=['GET', 'POST'])
def createWeeklyReport():
    # in case of post request, create weekly report and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        reportCreator = WeeklyReportCreationHandler(
            appConfig['weeklyRepCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = reportCreator.createWeeklyReport(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createWeeklyReport.html.j2')


@weeklyReportsPage.route('/list', defaults={'req_path': ''})
@weeklyReportsPage.route('/list/<path:req_path>')
def showWeeklyReport(req_path):
    BASE_DIR = appConfig['weeklyReportsFolderPath']

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    # https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    def fObjFromScan(x):
        return {'name': x.name,
                'mTime': getTimeStampString(
                    x.stat().st_mtime),
                'size': getReadableByteSize(x.stat().st_size)}
    fileObjs = [fObjFromScan(x) for x in os.scandir(abs_path)]
    return render_template('showDirectory.html.j2', data={'files': fileObjs,
                                                              'title': 'Weekly Reports',
                                                              'heading': 'Weekly Reports'})
