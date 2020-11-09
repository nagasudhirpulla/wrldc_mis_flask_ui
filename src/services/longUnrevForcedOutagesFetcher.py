import requests
import datetime as dt
from src.typeDefs.transOutagesFetchResp import ITransOutagesFetchResp


class LongUnrevForcedOutagesFetcher():
    fetchUrl = ''

    def __init__(self, fetchUrl):
        self.fetchUrl = fetchUrl

    def fetchLongTimeUnrevForcedOutages(self, startDate: dt.datetime, endDate: dt.datetime) -> ITransOutagesFetchResp:
        """fetch long time unrevived forced outages using the api service
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            ITransOutagesFetchResp: Result of the long time unrevived forced outages fetcher operation
        """
        fetchMajorGenOutagesPayload = {
            "startDate": dt.datetime.strftime(startDate, '%Y-%m-%d'),
            "endDate": dt.datetime.strftime(endDate, '%Y-%m-%d')
        }
        res = requests.get(self.fetchUrl,
                           params=fetchMajorGenOutagesPayload)

        operationResult: ITransOutagesFetchResp = {
            "isSuccess": False,
            'status': res.status_code,
            'data':  [],
            'message': 'Unable to fetch long time unrevived forced outages...'
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
