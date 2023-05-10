from pydantic import BaseModel


class SymbolGroupDataRow(BaseModel):
    symbol_id: str
    last: int
    close: int
    count: int
    volume: int
    value: int


class SymbolGroupAPIDataRow(SymbolGroupDataRow):
    short_name: str
    long_name: str
    change: int
    high: int
    low: int
    open: int
    yesterday: int
