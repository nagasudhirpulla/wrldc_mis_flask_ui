'''
This is the web server that acts as a service that creates outages raw data
'''
from src.appConfig import getConfig
from flask import Flask, request, jsonify, render_template
from src.routeControllers.oauth import login_manager, oauthPage
from src.security.errorHandlers import page_forbidden, page_not_found, page_unauthorized
from src.services.rawOutagesCreationHandler import RawOutagesCreationHandler
from src.services.rawPairAnglesCreationHandler import RawPairAnglesCreationHandler
from src.services.rawFreqCreationHandler import RawFrequencyCreationHandler
from src.services.rawVoltCreationHandler import RawVoltageCreationHandler
from src.services.derFreqCreationHandler import DerivedFrequencyCreationHandler
from src.services.derVoltCreationHandler import DerivedVoltageCreationHandler
from src.services.derVdiCreationHandler import DerivedVdiCreationHandler
from src.services.iegcViolMsgsHandler import IegcViolMsgsCreationHandler
from src.services.transmissionConstraintsHandler import TransmissionConstraintsCreationHandler
from src.services.ictConstraintsHandler import IctConstraintsCreationHandler
from src.services.highVoltageNodeCreationHandler import HighVoltageNodeCreationHandler
from src.services.lowVoltageNodeCreationHandler import LowVoltageNodeCreationHandler
from src.utils.stringUtils import getReadableByteSize, getTimeStampString
import datetime as dt
import pandas as pd
import json
import os
from waitress import serve
from src.routeControllers.createRawOutages import createRawOutagesPage
from src.routeControllers.weeklyReports import weeklyReportsPage
from src.routeControllers.violationReports import violationReportsPage
from src.routeControllers.monthlyReports import monthlyReportsPage
from src.routeControllers.derivedFreq import derviedFreqPage
from src.routeControllers.iegcViolMsgs import iegcViolMsgsPage
from src.routeControllers.outages import outagesPage
from src.routeControllers.transOutages import transOutagesPage
from src.routeControllers.majorGenOutages import majorGenOutagesPage
from src.routeControllers.longTimeUnrevForcedOutages import longUnrevForcedOutagesPage
from src.security.decorators import role_required
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from typing import Any, cast

# set this variable since we are currently not running this app on SSL
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

# get application config
appConfig = getConfig()

appPrefix = appConfig["appPrefix"]
if pd.isna(appPrefix):
    appPrefix = ""

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# limit max upload file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# valid file extensions
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']

# User session management setup
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('home.html.j2')


app.register_error_handler(401, page_unauthorized)
app.register_error_handler(403, page_forbidden)
app.register_error_handler(404, page_not_found)
app.register_blueprint(oauthPage, url_prefix='/oauth')
app.register_blueprint(createRawOutagesPage, url_prefix='/createRawOutages')
app.register_blueprint(derviedFreqPage, url_prefix='/derivedFreq')
app.register_blueprint(iegcViolMsgsPage, url_prefix='/iegcViolMsgs')
app.register_blueprint(outagesPage, url_prefix='/outages')
app.register_blueprint(transOutagesPage, url_prefix='/transOutages')
app.register_blueprint(majorGenOutagesPage, url_prefix='/majorGenOutages')
app.register_blueprint(longUnrevForcedOutagesPage,
                       url_prefix='/longUnrevForcedOutages')
app.register_blueprint(weeklyReportsPage,
                       url_prefix='/weeklyReports')
app.register_blueprint(violationReportsPage,
                       url_prefix='/violationReports')
app.register_blueprint(monthlyReportsPage,
                       url_prefix='/monthlyReports')


@app.route('/createRawPairAngles', methods=['GET', 'POST'])
@role_required('mis_admin')
def createRawPairAngles():
    # in case of post request, create raw pair angles and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        pairAnglesCreator = RawPairAnglesCreationHandler(
            appConfig['rawPairAnglesCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = pairAnglesCreator.createRawPairAngles(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawPairAngles.html.j2')


@app.route('/createRawFreq', methods=['GET', 'POST'])
@role_required('mis_admin')
def createRawFreq():
    # in case of post request, create raw freq and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        rawFreqCreator = RawFrequencyCreationHandler(
            appConfig['rawFrequencyCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = rawFreqCreator.createRawFrequency(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawFreq.html.j2')


@app.route('/createRawVolt', methods=['GET', 'POST'])
@role_required('mis_admin')
def createRawVolt():
    # in case of post request, create raw voltage and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        rawVoltCreator = RawVoltageCreationHandler(
            appConfig['rawVoltageCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = rawVoltCreator.createRawVoltage(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawVolt.html.j2')


@app.route('/createDerFreq', methods=['GET', 'POST'])
@role_required('mis_admin')
def createDerFreq():
    # in case of post request, create derived frequency and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        derFreqCreator = DerivedFrequencyCreationHandler(
            appConfig['derivedFrequencyCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = derFreqCreator.createDerivedFrequency(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createDerFreq.html.j2')


@app.route('/createDerVolt', methods=['GET', 'POST'])
@role_required('mis_admin')
def createDerVolt():
    # in case of post request, create derived voltage and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        derVoltCreator = DerivedVoltageCreationHandler(
            appConfig['derivedVoltageCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = derVoltCreator.createDerivedVoltage(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createDerVolt.html.j2')


@app.route('/createDerVdi', methods=['GET', 'POST'])
@role_required('mis_admin')
def createDerVdi():
    # in case of post request, create derived voltage and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        derVdiCreator = DerivedVdiCreationHandler(
            appConfig['derivedVdiCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = derVdiCreator.createDerivedVdi(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createDerVdi.html.j2')


@app.route('/createIegcViolMsgs', methods=['GET', 'POST'])
@role_required('mis_admin')
def createIegcViolMsgs():
    # in case of post request, create iegc violation messages and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createIegcViolMsgs.html.j2', data={'message': 'Only .xlsx files are supported'})
        iegcViolMsgsCreator = IegcViolMsgsCreationHandler(
            appConfig['iegcViolMsgsCreationServiceUrl'])
        resp = iegcViolMsgsCreator.createIegcViolMsgs(reqFile)
        return render_template('createIegcViolMsgs.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createIegcViolMsgs.html.j2')


@app.route('/createTransmissionConstraints', methods=['GET', 'POST'])
@role_required('mis_admin')
def createTransmissionConstraints():
    # in case of post request, create transmission constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createTransmissionConstraints.html.j2', data={'message': 'Only .xlsx files are supported'})
        transmissionConstraintsCreator = TransmissionConstraintsCreationHandler(
            appConfig['transmissionConstraintsCreationServiceUrl'])
        resp = transmissionConstraintsCreator.createTransmissionConstraints(
            reqFile)
        return render_template('createTransmissionConstraints.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createTransmissionConstraints.html.j2')


@app.route('/createIctConstraints', methods=['GET', 'POST'])
@role_required('mis_admin')
def createIctConstraints():
    # in case of post request, create ict constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createIctConstraints.html.j2', data={'message': 'Only .xlsx files are supported'})
        ictConstraintsCreator = IctConstraintsCreationHandler(
            appConfig['ictConstraintsCreationServiceUrl'])
        resp = ictConstraintsCreator.createIctConstraints(reqFile)
        return render_template('createIctConstraints.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createIctConstraints.html.j2')


@app.route('/createHighVoltageNodes', methods=['GET', 'POST'])
@role_required('mis_admin')
def createHighVoltageNodes():
    # in case of post request, create ict constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createHighVoltageNode.html.j2', data={'message': 'Only .xlsx files are supported'})
        highVoltageNodeCreator = HighVoltageNodeCreationHandler(
            appConfig['highVoltageNodeCreationServiceUrl'])
        resp = highVoltageNodeCreator.createHighVoltageNode(reqFile)
        return render_template('createHighVoltageNode.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createHighVoltageNode.html.j2')


@app.route('/createLowVoltageNodes', methods=['GET', 'POST'])
@role_required('mis_admin')
def createLowVoltageNodes():
    # in case of post request, create ict constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createLowVoltageNode.html.j2', data={'message': 'Only .xlsx files are supported'})
        lowVoltageNodeCreator = LowVoltageNodeCreationHandler(
            appConfig['lowVoltageNodeCreationServiceUrl'])
        resp = lowVoltageNodeCreator.createLowVoltageNode(reqFile)
        return render_template('createLowVoltageNode.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createLowVoltageNode.html.j2')


hostedApp = Flask(__name__)

cast(Any, hostedApp).wsgi_app = DispatcherMiddleware(NotFound(), {
    appPrefix: app
})

if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        hostedApp.run(host="0.0.0.0", port=int(
            appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(
            appConfig['flaskPort']), url_prefix=appPrefix, threads=1)
