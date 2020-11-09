import requests
import datetime as dt
from src.typeDefs.weeklyRepCreationResp import IWeeklyRepCreationResp


class WeeklyReportCreationHandler():
    weeklyReportCreationUrl = ''

    def __init__(self, weeklyReportCreationUrl):
        self.weeklyReportCreationUrl = weeklyReportCreationUrl

    def createWeeklyReport(self, startDate: dt.datetime, endDate: dt.datetime) -> IWeeklyRepCreationResp:
        """create weekly report using the api service

        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date

        Returns:
            IWeeklyRepCreationResp: Result of the weekly report creation operation
        """        
        createWeeklyReportPayload = {
            "startDate": dt.datetime.strftime(startDate, '%Y-%m-%d'),
            "endDate": dt.datetime.strftime(endDate, '%Y-%m-%d')
        }
        res = requests.post(self.weeklyReportCreationUrl,
                            json=createWeeklyReportPayload)

        operationResult: IWeeklyRepCreationResp = {
            "isSuccess": False,
            'status': res.status_code,
            'message': 'Unable to create weekly report...'
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
