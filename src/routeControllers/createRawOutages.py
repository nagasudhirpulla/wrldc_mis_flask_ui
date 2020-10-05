from flask import Blueprint, jsonify, render_template, request
from src.appConfig import getConfig
from src.services.rawOutagesCreationHandler import RawOutagesCreationHandler
import datetime as dt

# get application config
appConfig = getConfig()

createRawOutagesPage = Blueprint('createRawOutages', __name__,
                                 template_folder='templates')


@createRawOutagesPage.route('/', methods=['GET', 'POST'])
def createRawOutages():
    # in case of post request, create raw outages and return json response
    if request.method == 'POST':
        reqData = request.get_json()
        outagesCreator = RawOutagesCreationHandler(appConfig['rawOutagesCreationServiceUrl'])
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        resp = outagesCreator.createRawOutages(startDate, endDate)
        return jsonify(resp), resp['status']
    # in case of get request just return the html template
    return render_template('createRawOutages.html.j2')
