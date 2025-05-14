from flask import Blueprint, jsonify, render_template, request, abort, send_file
import datetime as dt
import os
from src.appConfig import getConfig
from src.utils.stringUtils import getReadableByteSize, getTimeStampString

# get application config
appConfig = getConfig()

violationReportsPage = Blueprint('violationReports', __name__,
                              template_folder='templates')


@violationReportsPage.route('/list', defaults={'req_path': '', 'folder': ''})
@violationReportsPage.route('/list/<path:folder>/<path:req_path>')
def showViolationReports(req_path, folder):
    if folder == "Violation":
        BASE_DIR = appConfig['violationReportsFolderPath']

    else:
        BASE_DIR = appConfig['atcReportsFolderPath']

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    return render_template('displayIegcViolMsgs.html.j2')
