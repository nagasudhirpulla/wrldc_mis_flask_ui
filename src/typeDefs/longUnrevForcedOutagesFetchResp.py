from typing import TypedDict, List
from src.typeDefs.outage import IOutage


class ILongTimeUnrevForcedOutagesFetchResp(TypedDict):
    isSuccess: bool
    status: int
    message: str
    data: List[IOutage]
