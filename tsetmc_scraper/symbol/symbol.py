from . import _core
from .group import SymbolGroupAPIDataRow, SymbolGroupDataRow
from .identification import SymbolIdDetails
from .info import SymbolClosingPriceInfo, SymbolInfo
from .notification import SymbolNotificationsDataRow
from .option import SymbolOptionData
from .orderbook import SymbolOrderBookData, SymbolOrderBookDataRow
from .price import SymbolDailyPriceDataRow, SymbolIntraDayPriceChartDataRow, SymbolPriceData, SymbolPriceOverview
from .shareholder import SymbolShareHolder, SymbolShareHolderDataRow
from .state_change import SymbolStateChangeDataRow
from .supervisor_message import SymbolSupervisorMessageDataRow
from .trade import SymbolTradeRow
from .traders_type import SymbolTradersTypeAPISubInfo, SymbolTradersTypeDataRow, SymbolTradersTypeInfo, SymbolTradersTypeSubInfo


class Symbol:
    def __init__(self, symbol_id: str):
        self.symbol_id = symbol_id

    def get_price_overview(self) -> SymbolPriceOverview:
        """
        gets the last price overview of the symbol and returns most of the information (in "dar yek negah" tab)
        """

        raw_data = _core.get_symbol_price_overview(symbol_id=self.symbol_id)

        tick = SymbolPriceData(
            last=raw_data["price_data"]["last"],
            close=raw_data["price_data"]["close"],
            open=raw_data["price_data"]["open"],
            yesterday=raw_data["price_data"]["yesterday"],
            high=raw_data["price_data"]["high"],
            low=raw_data["price_data"]["low"],
            count=raw_data["price_data"]["count"],
            volume=raw_data["price_data"]["volume"],
            value=raw_data["price_data"]["value"],
        )

        sell_rows = [
            SymbolOrderBookDataRow(
                count=row["count"],
                price=row["price"],
                volume=row["volume"],
            )
            for row in raw_data["orderbook_data"]["sell_rows"]
        ]
        buy_rows = [
            SymbolOrderBookDataRow(
                count=row["count"],
                price=row["price"],
                volume=row["volume"],
            )
            for row in raw_data["orderbook_data"]["buy_rows"]
        ]
        orderbook = SymbolOrderBookData(
            sell_rows=sell_rows,
            buy_rows=buy_rows,
        )

        traders_type = SymbolTradersTypeDataRow(
            legal=SymbolTradersTypeInfo(
                buy=SymbolTradersTypeSubInfo(
                    count=raw_data["traders_type_data"]["legal"]["buy"]["count"],
                    volume=raw_data["traders_type_data"]["legal"]["buy"]["volume"],
                    value=raw_data["traders_type_data"]["legal"]["buy"]["value"],
                ),
                sell=SymbolTradersTypeSubInfo(
                    count=raw_data["traders_type_data"]["legal"]["sell"]["count"],
                    volume=raw_data["traders_type_data"]["legal"]["sell"]["volume"],
                    value=raw_data["traders_type_data"]["legal"]["sell"]["value"],
                ),
            ),
            real=SymbolTradersTypeInfo(
                buy=SymbolTradersTypeSubInfo(
                    count=raw_data["traders_type_data"]["real"]["buy"]["count"],
                    volume=raw_data["traders_type_data"]["real"]["buy"]["volume"],
                    value=raw_data["traders_type_data"]["real"]["buy"]["value"],
                ),
                sell=SymbolTradersTypeSubInfo(
                    count=raw_data["traders_type_data"]["real"]["sell"]["count"],
                    volume=raw_data["traders_type_data"]["real"]["sell"]["volume"],
                    value=raw_data["traders_type_data"]["real"]["sell"]["value"],
                ),
            ),
        )

        group_data = [
            SymbolGroupDataRow(
                symbol_id=row["symbol_id"],
                last=row["last"],
                close=row["close"],
                count=row["count"],
                volume=row["volume"],
                value=row["value"],
            )
            for row in raw_data["group_data"]
        ]

        return SymbolPriceOverview(
            price_data=tick,
            orderbook=orderbook,
            traders_type=traders_type,
            group_data=group_data,
        )

    def get_info(self) -> SymbolInfo:
        """
        gets the symbol information such as EPS, Groupe PE, Flow, Flow Title, Base Volume and so on
        """

        raw_data = _core.get_symbol_info(symbol_id=self.symbol_id)

        return SymbolInfo(
            date=raw_data["date"],
            symbol_id=raw_data["symbol_id"],
            isin=raw_data["isin"],
            short_name=raw_data["short_name"],
            full_name=raw_data["full_name"],
            eps=raw_data["eps"],
            group_pe=raw_data["group_pe"],
            group_code=raw_data["group_code"],
            group_name=raw_data["group_name"],
            range_min=raw_data["range_min"],
            range_max=raw_data["range_max"],
            min_week=raw_data["min_week"],
            max_week=raw_data["max_week"],
            min_year=raw_data["min_year"],
            max_year=raw_data["max_year"],
            month_volume_avg=raw_data["month_volume_avg"],
            contract_size=raw_data["contract_size"],
            nav=raw_data["nav"],
            flow=raw_data["flow"],
            flow_title=raw_data["flow_title"],
            total_count=raw_data["total_count"],
            base_volume=raw_data["base_volume"],
        )

    def get_traders_type(self) -> SymbolTradersTypeDataRow:
        """
        gets the symbol traders type
        """

        raw_data = _core.get_symbol_traders_type(symbol_id=self.symbol_id)

        return SymbolTradersTypeDataRow(
            legal=SymbolTradersTypeInfo(
                buy=SymbolTradersTypeAPISubInfo(
                    count=raw_data["legal"]["buy"]["count"],
                    volume=raw_data["legal"]["buy"]["volume"],
                ),
                sell=SymbolTradersTypeAPISubInfo(
                    count=raw_data["legal"]["sell"]["count"],
                    volume=raw_data["legal"]["sell"]["volume"],
                ),
            ),
            real=SymbolTradersTypeInfo(
                buy=SymbolTradersTypeAPISubInfo(
                    count=raw_data["real"]["buy"]["count"],
                    volume=raw_data["real"]["buy"]["volume"],
                ),
                sell=SymbolTradersTypeAPISubInfo(
                    count=raw_data["real"]["sell"]["count"],
                    volume=raw_data["real"]["sell"]["volume"],
                ),
            ),
        )

    def get_orderbook(self) -> SymbolOrderBookData:
        """
        gets the symbol orderbook
        """

        raw_data = _core.get_symbol_orderbook(symbol_id=self.symbol_id)

        sell_rows = [
            SymbolOrderBookDataRow(
                count=row["count"],
                price=row["price"],
                volume=row["volume"],
            )
            for row in raw_data["sell_rows"]
        ]
        buy_rows = [
            SymbolOrderBookDataRow(
                count=row["count"],
                price=row["price"],
                volume=row["volume"],
            )
            for row in raw_data["buy_rows"]
        ]
        return SymbolOrderBookData(
            sell_rows=sell_rows,
            buy_rows=buy_rows,
        )

    def get_closing_price_info(self) -> SymbolClosingPriceInfo:
        """
        gets the symbol current closing price info
        """

        raw_data = _core.get_symbol_closing_price_info(symbol_id=self.symbol_id)

        return SymbolClosingPriceInfo(
            date=raw_data["date"],
            time=raw_data["time"],
            state_value=raw_data["state_value"].strip(),
            state_title=raw_data["state_title"].strip(),
            price_change=raw_data["price_change"],
            low=raw_data["low"],
            high=raw_data["high"],
            yesterday=raw_data["yesterday"],
            open=raw_data["open"],
            close=raw_data["close"],
            last=raw_data["last"],
            count=raw_data["count"],
            volume=raw_data["volume"],
            value=raw_data["value"],
        )

    def get_group_data(self, group_code: int | None = None) -> list[SymbolGroupAPIDataRow]:
        """
        gets related companies (companies in the same group)
        in case of group_code being None, we'll call get_info to get the group_code for the current symbol
        """

        if group_code is None:
            group_code = self.get_info().group_code

        raw_data = _core.get_symbol_group_data(symbol_group_code=group_code)

        return [
            SymbolGroupAPIDataRow(
                symbol_id=row["symbol_id"],
                short_name=row["short_name"],
                long_name=row["long_name"],
                last=row["last"],
                close=row["close"],
                count=row["count"],
                volume=row["volume"],
                value=row["value"],
                change=row["change"],
                high=row["high"],
                low=row["low"],
                open=row["open"],
                yesterday=row["yesterday"],
            )
            for row in raw_data
        ]

    def get_option_data(self, isin: str | None = None) -> SymbolOptionData:
        """
        gets data for option symbols
        in case of isin being None, we'll call get_info to get the isin for the current symbol
        """

        if isin is None:
            isin = self.get_info().isin

        raw_data = _core.get_symbol_option_data(symbol_isin=isin)

        return SymbolOptionData(
            symbol_id=raw_data["symbol_id"],
            isin=raw_data["isin"],
            base_symbol_id=raw_data["base_symbol_id"],
            buy_op=raw_data["buy_op"],
            sell_op=raw_data["sell_op"],
            contract_size=raw_data["contract_size"],
            strike_price=raw_data["strike_price"],
            begin_date=raw_data["begin_date"],
            end_date=raw_data["end_date"],
            a_factor=raw_data["a_factor"],
            b_factor=raw_data["b_factor"],
            c_factor=raw_data["c_factor"],
        )

    def get_intraday_trades(self) -> list[SymbolTradeRow]:
        """
        gets last days intraday trade list
        """

        raw_data = _core.get_symbol_intraday_trades(symbol_id=self.symbol_id)

        return [
            SymbolTradeRow(
                time=row["time"],
                volume=row["volume"],
                price=row["price"],
                canceled=row["canceled"],
            )
            for row in raw_data
        ]

    def get_intraday_price_chart_data(self) -> list[SymbolIntraDayPriceChartDataRow]:
        """
        gets last days intraday price chart (in "dar yek negah" tab)
        """

        raw_data = _core.get_symbol_intraday_price_chart(symbol_id=self.symbol_id)

        ticks = [
            SymbolIntraDayPriceChartDataRow(
                time=row["time"],
                high=row["high"],
                low=row["low"],
                open=row["open"],
                close=row["close"],
                volume=row["volume"],
            )
            for row in raw_data
        ]

        return ticks

    def get_supervisor_messages_data(self) -> list[SymbolSupervisorMessageDataRow]:
        """
        get list of supervisor messages (in "payame nazer" tab)
        """

        raw_data = _core.get_symbol_supervisor_messages(symbol_id=self.symbol_id)

        messages = [
            SymbolSupervisorMessageDataRow(
                datetime=row["datetime"],
                title=row["title"],
                content=row["content"],
            )
            for row in raw_data
        ]

        return messages

    def get_notifications_data(self) -> list[SymbolNotificationsDataRow]:
        """
        get list of notifications (in "etelaiye ha" tab)
        """

        raw_data = _core.get_symbol_notifications(symbol_id=self.symbol_id)

        notifications = [
            SymbolNotificationsDataRow(
                datetime=row["datetime"],
                title=row["title"],
            )
            for row in raw_data
        ]

        return notifications

    def get_state_changes_data(self) -> list[SymbolStateChangeDataRow]:
        """
        get list of state changes (in "taghire vaziat" tab)
        """

        raw_data = _core.get_symbol_state_changes(symbol_id=self.symbol_id)

        state_changes = [
            SymbolStateChangeDataRow(
                datetime=row["datetime"],
                new_state=row["new_state"],
            )
            for row in raw_data
        ]

        return state_changes

    def get_daily_history(self) -> list[SymbolDailyPriceDataRow]:
        """
        get list of daily ticks history (in "sabeghe" tab)
        """

        raw_data = _core.get_symbol_daily_ticks_history(symbol_id=self.symbol_id)

        return [
            SymbolDailyPriceDataRow(
                date=row["date"],
                time=row["time"],
                last=row["last"],
                close=row["close"],
                open=row["open"],
                yesterday=row["yesterday"],
                change=row["change"],
                high=row["high"],
                low=row["low"],
                count=row["count"],
                volume=row["volume"],
                value=row["value"],
            )
            for row in raw_data
        ]

    def get_id_details(self) -> SymbolIdDetails:
        """
        gets symbol identity details and returns all the information (in "shenase" tab)
        """

        raw_data = _core.get_symbol_id_details(symbol_id=self.symbol_id)

        details = SymbolIdDetails(
            isin=raw_data["isin"],
            short_isin=raw_data["short_isin"],
            short_name=raw_data["short_name"],
            long_name=raw_data["long_name"],
            english_name=raw_data["english_name"],
            company_isin=raw_data["company_isin"],
            company_short_isin=raw_data["company_short_isin"],
            company_name=raw_data["company_name"],
            market_code=raw_data["market_code"],
            market_name=raw_data["market_name"],
            group_code=raw_data["group_code"],
            group_name=raw_data["group_name"],
            subgroup_code=raw_data["subgroup_code"],
            subgroup_name=raw_data["subgroup_name"],
        )

        return details

    def get_traders_type_history(self) -> list[SymbolTradersTypeDataRow]:
        """
        returns daily traders type history (in "haghihi-hoghooghi" tab)
        """

        raw_data = _core.get_symbol_traders_type_history(symbol_id=self.symbol_id)

        traders_type_history = [
            SymbolTradersTypeDataRow(
                legal=SymbolTradersTypeInfo(
                    buy=SymbolTradersTypeSubInfo(
                        count=row["legal"]["buy"]["count"],
                        volume=row["legal"]["buy"]["volume"],
                        value=row["legal"]["buy"]["value"],
                    ),
                    sell=SymbolTradersTypeSubInfo(
                        count=row["legal"]["sell"]["count"],
                        volume=row["legal"]["sell"]["volume"],
                        value=row["legal"]["sell"]["value"],
                    ),
                ),
                real=SymbolTradersTypeInfo(
                    buy=SymbolTradersTypeSubInfo(
                        count=row["real"]["buy"]["count"],
                        volume=row["real"]["buy"]["volume"],
                        value=row["real"]["buy"]["value"],
                    ),
                    sell=SymbolTradersTypeSubInfo(
                        count=row["real"]["sell"]["count"],
                        volume=row["real"]["sell"]["volume"],
                        value=row["real"]["sell"]["value"],
                    ),
                ),
            )
            for row in raw_data
        ]

        return traders_type_history

    def get_shareholders_data(self) -> list[SymbolShareHolderDataRow]:
        """
        returns list of major shareholders (in "saham daran" tab)
        """

        company_isin = self.get_id_details().company_isin
        raw_data = _core.get_symbol_shareholders(company_isin=company_isin)

        shareholders = [
            SymbolShareHolderDataRow(
                shareholder=SymbolShareHolder(
                    _company_isin=company_isin,
                    id=row["id"],
                    name=row["name"],
                ),
                count=row["count"],
                percentage=row["percentage"],
                change=row["change"],
            )
            for row in raw_data
        ]

        return shareholders
