from typing import TypedDict


class IegcViolMsgsFetchResp(TypedDict):
    isSuccess: bool
    status: int
    message: str
    data: list