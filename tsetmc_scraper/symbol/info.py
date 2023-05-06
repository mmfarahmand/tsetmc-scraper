from jdatetime import date as jdate
from pydantic import BaseModel


class SymbolInfo(BaseModel):
    date: jdate
    symbol_id: str
    isin: str
    short_name: str
    full_name: str
    eps: int | None
    group_pe: float
    group_code: int
    group_name: str
    range_min: int
    range_max: int
    min_week: int
    max_week: int
    min_year: int
    max_year: int
    month_volume_avg: int
    contract_size: int
    nav: int
    flow: int
    flow_title: str
    total_count: int
    base_volume: int

    class Config:
        arbitrary_types_allowed = True
