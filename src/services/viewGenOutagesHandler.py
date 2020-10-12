import requests
import datetime as dt
from src.typeDefs.rawOutagesCreationResp import RawOutagesCreationResp


class ViewGenOutagesHandler():
    rawOutagesCreationUrl = ''

    def __init__(self, rawOutagesCreationUrl):
        self.rawOutagesCreationUrl = rawOutagesCreationUrl

    def viewGenOutages(self, startDate: dt.datetime, endDate: dt.datetime,outageType:str) -> RawOutagesCreationResp:
        """create raw outages using the api service

        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date

        Returns:
            RawOutagesCreationResp: Result of the raw outages creation operation
        """        
        res = requests.get(self.rawOutagesCreationUrl,json={"startDate":startDate, "endDate":endDate,"outageType":outageType})

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
            try:
                resJSON = res.json()
                operationResult['message'] = resJSON['message']
            except ValueError:
                operationResult['message'] = res.text
        return operationResult
