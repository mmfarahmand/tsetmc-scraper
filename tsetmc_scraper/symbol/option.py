from jdatetime import date as jdate
from pydantic import BaseModel


class SymbolOptionData(BaseModel):
    symbol_id: str
    isin: str
    base_symbol_id: str
    buy_op: int
    sell_op: int
    contract_size: int
    strike_price: int
    begin_date: jdate
    end_date: jdate
    a_factor: float
    b_factor: float
    c_factor: int

    class Config:
        arbitrary_types_allowed = True
