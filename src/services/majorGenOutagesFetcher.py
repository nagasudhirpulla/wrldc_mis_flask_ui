import requests
import datetime as dt
from src.typeDefs.transOutagesFetchResp import ITransOutagesFetchResp


class MajorGenOutagesFetcher():
    majorOutagesFetchUrl = ''

    def __init__(self, majorOutagesFetchUrl):
        self.majorOutagesFetchUrl = majorOutagesFetchUrl

    def fetchMajorGenOutages(self, startDate: dt.datetime, endDate: dt.datetime) -> ITransOutagesFetchResp:
        """fetch major generating unit outages using the api service
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            ITransOutagesFetchResp: Result of the major generating unit outages fetcher operation
        """
        fetchMajorGenOutagesPayload = {
            "startDate": dt.datetime.strftime(startDate, '%Y-%m-%d'),
            "endDate": dt.datetime.strftime(endDate, '%Y-%m-%d')
        }
        res = requests.get(self.majorOutagesFetchUrl,
                           params=fetchMajorGenOutagesPayload)

        operationResult: ITransOutagesFetchResp = {
            "isSuccess": False,
            'status': res.status_code,
            'data':  [],
            'message': 'Unable to fetch major generating unit outages...'
        }

        if res.status_code == requests.codes['ok']:
            resJSON = res.json()
            operationResult['isSuccess'] = True
            operationResult['data'] = resJSON['data']
            operationResult['message'] = resJSON['message']
        else:
            operationResult['isSuccess'] = False
            try:
                resJSON = res.json()
                operationResult['message'] = resJSON['message']
            except ValueError:
                operationResult['message'] = res.text
        return operationResult
