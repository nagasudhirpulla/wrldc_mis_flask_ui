from typing import TypedDict


class IAppConfig(TypedDict):
    flaskSecret: str
    flaskPort: str
    mode: str
    rawOutagesCreationServiceUrl: str
    rawPairAnglesCreationServiceUrl: str
    rawFrequencyCreationServiceUrl: str
    rawVoltageCreationServiceUrl: str
    derivedFrequencyCreationServiceUrl: str
    derivedVoltageCreationServiceUrl: str
    derivedVdiCreationServiceUrl: str
    iegcViolMsgsCreationServiceUrl: str
    transmissionConstraintsCreationServiceUrl: str
    ictConstraintsCreationServiceUrl: str
    highVoltageNodeCreationServiceUrl: str
    lowVoltageNodeCreationServiceUrl: str
    weeklyRepCreationServiceUrl: str
    weeklyReportsFolderPath: str
    derivedFrequencyFetchUrl: str
    iegcViolMsgsFetchUrl: str
    outagesFetchUrl: str
    transOutagesFetchUrl: str
    majorGenOutagesFetchUrl: str
    longUnrevForcedOutagesFetchUrl: str
