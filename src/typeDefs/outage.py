from typing import TypedDict


class IOutage(TypedDict):
    elName: str
    owners: str
    capacity: str
    outageDate: str
    outageTime: str
    revivalDate: str
    revivalTime: str
    reason: str