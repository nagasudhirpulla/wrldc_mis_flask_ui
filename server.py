'''
This is the web server that acts as a service that creates outages raw data
'''
from src.appConfig import getConfig
from flask import Flask, request, jsonify, render_template
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
import datetime as dt
import pandas as pd
import json,requests
import os
from waitress import serve
from src.routeControllers.createRawOutages import createRawOutagesPage

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# limit max upload file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# valid file extensions
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']


@app.route('/')
def hello():
    return render_template('home.html.j2')

app.register_blueprint(createRawOutagesPage, url_prefix='/createRawOutages')

@app.route('/viewOutages', methods=['GET', 'POST'])
def viewOutages():
    # in case of post request, create raw outages and return json response
    if request.method == 'POST':
        from_ = request.form.get('startDate')
        to_ = request.form.get('endDate')
        # reqData = request.get_json()
        # outagesCreator = RawOutagesCreationHandler(appConfig['rawOutagesCreationServiceUrl'])
        # startDate = dt.datetime.strptime(from_, '%Y-%m-%d')
        # endDate = dt.datetime.strptime(to_, '%Y-%m-%d')
        # resp = outagesCreator.createRawOutages(startDate, endDate)
        resp = requests.get(appConfig['rawOutagesCreationServiceUrl2'],json={"startDate":from_,"endDate":to_})
        print(resp.json())
        print(resp.status_code)
        return render_template('viewOutages.html.j2',res=resp.json())

    # in case of get request just return the html template
    return render_template('viewOutages.html.j2')

@app.route('/createRawPairAngles', methods=['GET', 'POST'])
def createRawPairAngles():
    # in case of post request, create raw pair angles and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        pairAnglesCreator = RawPairAnglesCreationHandler(appConfig['rawPairAnglesCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = pairAnglesCreator.createRawPairAngles(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawPairAngles.html.j2')


@app.route('/createRawFreq', methods=['GET', 'POST'])
def createRawFreq():
    # in case of post request, create raw freq and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        rawFreqCreator = RawFrequencyCreationHandler(appConfig['rawFrequencyCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = rawFreqCreator.createRawFrequency(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawFreq.html.j2')


@app.route('/createRawVolt', methods=['GET', 'POST'])
def createRawVolt():
    # in case of post request, create raw voltage and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        rawVoltCreator = RawVoltageCreationHandler(appConfig['rawVoltageCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = rawVoltCreator.createRawVoltage(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawVolt.html.j2')


@app.route('/createDerFreq', methods=['GET', 'POST'])
def createDerFreq():
    # in case of post request, create derived frequency and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        derFreqCreator = DerivedFrequencyCreationHandler(appConfig['derivedFrequencyCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = derFreqCreator.createDerivedFrequency(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createDerFreq.html.j2')


@app.route('/createDerVolt', methods=['GET', 'POST'])
def createDerVolt():
    # in case of post request, create derived voltage and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        derVoltCreator = DerivedVoltageCreationHandler(appConfig['derivedVoltageCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = derVoltCreator.createDerivedVoltage(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createDerVolt.html.j2')


@app.route('/createDerVdi', methods=['GET', 'POST'])
def createDerVdi():
    # in case of post request, create derived voltage and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        derVdiCreator = DerivedVdiCreationHandler(appConfig['derivedVdiCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = derVdiCreator.createDerivedVdi(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createDerVdi.html.j2')


@app.route('/createIegcViolMsgs', methods=['GET', 'POST'])
def createIegcViolMsgs():
    # in case of post request, create iegc violation messages and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createIegcViolMsgs.html.j2', data={'message': 'Only .xlsx files are supported'})
        iegcViolMsgsCreator = IegcViolMsgsCreationHandler(appConfig['iegcViolMsgsCreationServiceUrl'])
        resp = iegcViolMsgsCreator.createIegcViolMsgs(reqFile)
        return render_template('createIegcViolMsgs.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createIegcViolMsgs.html.j2')


@app.route('/createTransmissionConstraints', methods=['GET', 'POST'])
def createTransmissionConstraints():
    # in case of post request, create transmission constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createTransmissionConstraints.html.j2', data={'message': 'Only .xlsx files are supported'})
        transmissionConstraintsCreator = TransmissionConstraintsCreationHandler(appConfig['transmissionConstraintsCreationServiceUrl'])
        resp = transmissionConstraintsCreator.createTransmissionConstraints(
            reqFile)
        return render_template('createTransmissionConstraints.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createTransmissionConstraints.html.j2')


@app.route('/createIctConstraints', methods=['GET', 'POST'])
def createIctConstraints():
    # in case of post request, create ict constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createIctConstraints.html.j2', data={'message': 'Only .xlsx files are supported'})
        ictConstraintsCreator = IctConstraintsCreationHandler(appConfig['ictConstraintsCreationServiceUrl'])
        resp = ictConstraintsCreator.createIctConstraints(reqFile)
        return render_template('createIctConstraints.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createIctConstraints.html.j2')


@app.route('/createHighVoltageNode', methods=['GET', 'POST'])
def createHighVoltageNode():
    # in case of post request, create ict constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createHighVoltageNode.html.j2', data={'message': 'Only .xlsx files are supported'})
        highVoltageNodeCreator = HighVoltageNodeCreationHandler(appConfig['highVoltageNodeCreationServiceUrl'])
        resp = highVoltageNodeCreator.createHighVoltageNode(reqFile)
        return render_template('createHighVoltageNode.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createHighVoltageNode.html.j2')


@app.route('/createLowVoltageNode', methods=['GET', 'POST'])
def createLowVoltageNode():
    # in case of post request, create ict constraints data and return reponse
    if request.method == 'POST':
        reqFile = request.files.get('inpFile')
        filename = reqFile.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.xlsx']:
                return render_template('createLowVoltageNode.html.j2', data={'message': 'Only .xlsx files are supported'})
        lowVoltageNodeCreator = LowVoltageNodeCreationHandler(appConfig['lowVoltageNodeCreationServiceUrl'])
        resp = lowVoltageNodeCreator.createLowVoltageNode(reqFile)
        return render_template('createLowVoltageNode.html.j2', data={'message': json.dumps(resp)})
    # in case of get request just return the html template
    return render_template('createLowVoltageNode.html.j2')


if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)
