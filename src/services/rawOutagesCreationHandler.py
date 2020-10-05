import requests
import datetime as dt
from src.typeDefs.rawOutagesCreationResp import RawOutagesCreationResp


class RawOutagesCreationHandler():
    rawOutagesCreationUrl = ''

    def __init__(self, rawOutagesCreationUrl):
        self.rawOutagesCreationUrl = rawOutagesCreationUrl

    def createRawOutages(self, startDate: dt.datetime, endDate: dt.datetime) -> RawOutagesCreationResp:
        """create raw outages using the api service

        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date

        Returns:
            RawOutagesCreationResp: Result of the raw outages creation operation
        """        
        createRawOutagesPayload = {
            "startDate": dt.datetime.strftime(startDate, '%Y-%m-%d'),
            "endDate": dt.datetime.strftime(endDate, '%Y-%m-%d')
        }
        res = requests.post(self.rawOutagesCreationUrl,json=createRawOutagesPayload)

        operationResult: RawOutagesCreationResp = {
            "isSuccess": False,
            'status': res.status_code,
            'message': 'Unable to create raw outages...'
        }

        if res.status_code == requests.codes['ok']:
            resJSON = res.json()
            operationResult['isSuccess'] = True
            operationResult['message'] = resJSON['message']
        else:
            operationResult['isSuccess'] = False
            try:
                resJSON = res.json()
                operationResult['message'] = resJSON['message']
            except ValueError:
                operationResult['message'] = res.text
        return operationResult
