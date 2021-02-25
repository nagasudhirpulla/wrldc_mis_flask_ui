from flask import Blueprint, jsonify, render_template, request, abort, send_file, redirect
import datetime as dt
import os
from src.appConfig import getConfig
from src.utils.stringUtils import getReadableByteSize, getTimeStampString
from src.security.decorators import role_required

# get application config
appConfig = getConfig()

monthlyReportsPage = Blueprint('monthlyReports', __name__,
                               template_folder='templates')


@monthlyReportsPage.route('/create', methods=['GET', 'POST'])
def createMonthlyReport():
    # in case of post request, create monthly report and return json response
    if request.method == 'POST':
        BASE_DIR = appConfig['monthlyReportsFolderPath']
        repName = "Monthly_Report_January 2021.docx"
        # Joining the base and the file path
        abs_path = os.path.join(BASE_DIR, repName)
        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)
        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path, as_attachment=True)
    # in case of get request just return the html template
    return render_template('createMonthlyReport.html.j2')
