from typing import TypedDict, List
from src.typeDefs.outage import IOutage


class ITransOutagesFetchResp(TypedDict):
    isSuccess: bool
    status: int
    message: str
    data: List[IOutage]
