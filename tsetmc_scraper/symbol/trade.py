from jdatetime import time as jtime
from pydantic import BaseModel


class SymbolTradeRow(BaseModel):
    time: jtime
    volume: int
    price: int
    canceled: int

    class Config:
        arbitrary_types_allowed = True
