from pydantic import BaseModel


class SymbolTradersTypeSubInfo(BaseModel):
    count: int
    volume: int
    value: int


class SymbolTradersTypeAPISubInfo(BaseModel):
    count: int
    volume: int


class SymbolTradersTypeInfo(BaseModel):
    buy: SymbolTradersTypeSubInfo | SymbolTradersTypeAPISubInfo
    sell: SymbolTradersTypeSubInfo | SymbolTradersTypeAPISubInfo


class SymbolTradersTypeDataRow(BaseModel):
    legal: SymbolTradersTypeInfo
    real: SymbolTradersTypeInfo
