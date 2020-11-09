import requests
import datetime as dt
from src.typeDefs.derFreqFetchResp import DerivedFreqFetchResp


class DerivedFrequencyFetcher():
    derivedFrequencyFetchUrl = ''

    def __init__(self, derivedFrequencyFetchUrl):
        self.derivedFrequencyFetchUrl = derivedFrequencyFetchUrl

    def fetchDerivedFrequency(self, startDate: dt.datetime, endDate: dt.datetime) -> DerivedFreqFetchResp:
        """display derived Frequency using the api service
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            DerivedFrequencyDisplayResp: Result of the derivedFrequency display operation
        """
        createDerivedFrequencyPayload = {
            "startDate": dt.datetime.strftime(startDate, '%Y-%m-%d'),
            "endDate": dt.datetime.strftime(endDate, '%Y-%m-%d')
        }
        res = requests.get(self.derivedFrequencyFetchUrl,
                            params=createDerivedFrequencyPayload)
        # print(res)
        # print(type(res))
        # print(res.status_code)
        # print(res.get_json())

        operationResult: DerivedFreqFetchResp = {
            "isSuccess": False,
            'status': res.status_code,
            'message': 'Unable to fetch derived Frequency...',
            'data': {'rows': [], 'weeklyFDI': -1}
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
                # print(resJSON['message'])
                operationResult['message'] = resJSON['message']
            except ValueError:
                operationResult['message'] = res.text
                # print(res.text)
        return operationResult
