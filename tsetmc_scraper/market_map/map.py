from enum import Enum

from pydantic import BaseModel
from pydantic.utils import deep_update

from . import _core


class MapDataRow(BaseModel):
    symbol_id: str
    symbol_short_name: str
    symbol_long_name: str

    close: int
    last: int
    volume: int
    value: int
    count: int

    group_name: str

    color: str
    price_change_percent: float
    percent: float


class MapType(Enum):
    MARKET_VALUE = 1
    MARKET_VOLUME = 2


class MarketMap:
    def __init__(self):
        self._heven = 0

        self._last_map_data = {}

    def get_market_map_data(self, map_type: MapType = MapType.MARKET_VALUE) -> dict[str, MapDataRow]:
        """
        Returns symbol data in the market map section ("naghshe bazar") page. Note that the webserver may occasionally throw a 403 error, in which case you should wait a few seconds and retry.
        """

        raw_data, new_heven = _core.get_market_map_data(map_type=map_type.value, heven=self._heven)

        self._last_map_data = deep_update(self._last_map_data, raw_data)

        map_data = {
            key: MapDataRow(
                symbol_id=data["symbol_id"],
                symbol_short_name=data["symbol_short_name"],
                symbol_long_name=data["symbol_long_name"],
                close=data["close"],
                last=data["last"],
                volume=data["volume"],
                value=data["value"],
                count=data["count"],
                group_name=data["group_name"],
                color=data["color"],
                price_change_percent=data["price_change_percent"],
                percent=data["percent"],
            )
            for key, data in raw_data.items()
        }

        return map_data
