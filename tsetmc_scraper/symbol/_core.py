import ast
import locale
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from jdatetime import date as jdate
from jdatetime import datetime as jdatetime
from jdatetime import time as jtime

from ..utils import convert_deven_to_jdate, convert_heven_to_jtime, get_request_headers


def get_symbol_intraday_price_chart(symbol_id: str) -> list[dict]:
    response = requests.get(
        url="http://www.tsetmc.com/tsev2/chart/data/IntraDayPrice.aspx",
        params={"i": symbol_id},
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    ticks = response.split(";")
    ticks = [t for t in ticks if t]  # remove empty string

    result = []
    for tick in ticks:
        tick = tick.split(",")
        hour, minute = tick[0].split(":")
        result.append(
            {
                "time": jtime(hour=int(hour), minute=int(minute)),
                "high": tick[1],
                "low": tick[2],
                "open": tick[3],
                "close": tick[4],
                "volume": tick[5],
            }
        )

    return result


def get_symbol_price_overview(symbol_id: str) -> dict:
    response = requests.get(
        url="http://www.tsetmc.com/tsev2/data/instinfodata.aspx",
        params={
            "i": symbol_id,
            "c": 27,
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    all_sections = response.split(";")

    # price section
    data = all_sections[0].split(",")
    price_data = {
        "last": int(data[2]),
        "close": int(data[3]),
        "open": int(data[4]),
        "yesterday": int(data[5]),
        "high": int(data[6]),
        "low": int(data[7]),
        "count": int(data[8]),
        "volume": int(data[9]),
        "value": int(data[10]),
    }

    # orderbook section
    data = all_sections[2].split(",")
    buy_book = []
    sell_book = []
    for row in data:
        if not row:
            continue

        sell_count, sell_volume, sell_price, buy_price, buy_volume, buy_count = row.split("@")
        buy_book.append(
            {
                "count": int(buy_count),
                "price": int(buy_price),
                "volume": int(buy_volume),
            }
        )
        sell_book.append(
            {
                "count": int(sell_count),
                "price": int(sell_price),
                "volume": int(sell_volume),
            }
        )
    orderbook = {
        "buy_rows": buy_book,
        "sell_rows": sell_book,
    }

    # traders_type section
    data = all_sections[4].split(",")
    data = [d for d in data if d]  # remove the empty string
    data = data if data else [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # arbitrary data in case of empty data
    r_buy_v, l_buy_v, _, r_sell_v, l_sell_v, r_buy_c, l_buy_c, _, r_sell_c, l_sell_c = data
    traders_type = {
        "legal": {
            "buy": {
                "value": int(l_buy_v) * price_data["close"],
                "volume": int(l_buy_v),
                "count": int(l_buy_c),
            },
            "sell": {
                "value": int(l_sell_v) * price_data["close"],
                "volume": int(l_sell_v),
                "count": int(l_sell_c),
            },
        },
        "real": {
            "buy": {
                "value": int(r_buy_v) * price_data["close"],
                "volume": int(r_buy_v),
                "count": int(r_buy_c),
            },
            "sell": {
                "value": int(r_sell_v) * price_data["close"],
                "volume": int(r_sell_v),
                "count": int(r_sell_c),
            },
        },
    }

    # group_live_data section
    data = all_sections[5].split(",")
    group_data = []
    for row in data:
        if not row:
            continue

        s_id, last, close, _, count, volume, value = row.split("@")
        group_data.append(
            {
                "symbol_id": s_id,
                "last": int(last),
                "close": int(close),
                "count": int(count),
                "volume": int(volume),
                "value": int(value),
            }
        )

    return {
        "price_data": price_data,
        "orderbook_data": orderbook,
        "traders_type_data": traders_type,
        "group_data": group_data,
    }


def get_symbol_info(symbol_id: str) -> dict:
    response = requests.get(
        url=f"http://cdn.tsetmc.com/api/Instrument/GetInstrumentInfo/{symbol_id}",
        params={},
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.json()["instrumentInfo"]

    date = convert_deven_to_jdate(response["dEven"])

    return {
        "date": date,
        "symbol_id": response["insCode"],
        "isin": response["instrumentID"],
        "short_name": response["lVal18AFC"],
        "full_name": response["lVal30"],
        "eps": response["eps"]["estimatedEPS"],
        "group_pe": response["eps"]["sectorPE"],
        "group_code": response["sector"]["cSecVal"],
        "group_name": response["sector"]["lSecVal"],
        "range_min": response["staticThreshold"]["psGelStaMin"],
        "range_max": response["staticThreshold"]["psGelStaMax"],
        "min_week": response["minWeek"],
        "max_week": response["maxWeek"],
        "min_year": response["minYear"],
        "max_year": response["maxYear"],
        "month_volume_avg": response["qTotTran5JAvg"],
        "contract_size": response["contractSize"],
        "nav": response["nav"],
        "flow": response["flow"],
        "flow_title": response["flowTitle"],
        "total_count": response["zTitad"],
        "base_volume": response["baseVol"],
    }


def get_symbol_traders_type(symbol_id: str) -> dict:
    response = requests.get(
        url=f"http://cdn.tsetmc.com/api/ClientType/GetClientType/{symbol_id}/1/0",
        params={},
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.json()["clientType"]

    return {
        "legal": {
            "buy": {
                "volume": response["buy_N_Volume"],
                "count": response["buy_CountN"],
            },
            "sell": {
                "volume": response["sell_N_Volume"],
                "count": response["sell_CountN"],
            },
        },
        "real": {
            "buy": {
                "volume": response["buy_I_Volume"],
                "count": response["buy_CountI"],
            },
            "sell": {
                "volume": response["sell_I_Volume"],
                "count": response["sell_CountI"],
            },
        },
    }


def get_symbol_orderbook(symbol_id: str) -> list[dict]:
    response = requests.get(
        url=f"http://cdn.tsetmc.com/api/BestLimits/{symbol_id}",
        params={},
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.json()["bestLimits"]
    response = sorted(response, key=lambda x: x["number"])

    order_map = {"buy_rows": [], "sell_rows": []}
    for row in response:
        buy_row = {
            "count": row["zOrdMeDem"],
            "price": row["pMeDem"],
            "volume": row["qTitMeDem"],
        }
        sell_row = {
            "count": row["zOrdMeOf"],
            "price": row["pMeOf"],
            "volume": row["qTitMeOf"],
        }

        index = row["number"] - 1

        while len(order_map["buy_rows"]) < index + 1:
            order_map["buy_rows"].append(None)

        while len(order_map["sell_rows"]) < index + 1:
            order_map["sell_rows"].append(None)

        order_map["buy_rows"][index] = buy_row
        order_map["sell_rows"][index] = sell_row

    return order_map


def get_symbol_closing_price_info(symbol_id: str) -> list[dict]:
    response = requests.get(
        url=f"http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{symbol_id}",
        params={},
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.json()["closingPriceInfo"]

    return {
        "date": convert_deven_to_jdate(deven=response["finalLastDate"]),
        "time": convert_heven_to_jtime(heven=response["lastHEven"]),
        "state_value": response["instrumentState"]["cEtaval"],
        "state_title": response["instrumentState"]["cEtavalTitle"],
        "price_change": response["priceChange"],
        "low": response["priceMin"],
        "high": response["priceMax"],
        "yesterday": response["priceYesterday"],
        "open": response["priceFirst"],
        "close": response["pClosing"],
        "last": response["pDrCotVal"],
        "count": response["zTotTran"],
        "volume": response["qTotTran5J"],
        "value": response["qTotCap"],
    }


def get_symbol_supervisor_messages(symbol_id: str) -> list[dict]:
    response = requests.get(
        url=" http://tsetmc.ir/Loader.aspx",
        params={
            "i": symbol_id,
            "Partree": "15131W",
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    soup = BeautifulSoup(response, "lxml")

    trs = soup.find("div", {"class": "content"}).table.tbody.find_all("tr")
    messages = []
    last_item = None
    for tr in trs:
        if last_item is None:
            ths = tr.find_all("th")
            title = ths[0].text.strip()
            dtime = jdatetime.strptime(ths[1].text.strip(), "%y/%m/%d %H:%M")
            last_item = {
                "datetime": dtime,
                "title": title,
            }
        else:
            last_item["content"] = tr.td.text.strip()
            messages.append(last_item)
            last_item = None

    return messages


def get_symbol_daily_ticks_history(symbol_id: str) -> list[dict]:
    response = requests.get(
        url=f"http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{symbol_id}/0",
        params={},
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.json()["closingPriceDaily"]

    return [
        {
            "date": convert_deven_to_jdate(row["dEven"]),
            "time": convert_heven_to_jtime(row["hEven"]),
            "open": row["priceFirst"],
            "high": row["priceMax"],
            "low": row["priceMin"],
            "close": row["pClosing"],
            "last": row["pDrCotVal"],
            "yesterday": row["priceYesterday"],
            "change": row["priceChange"],
            "value": row["qTotCap"],
            "volume": row["qTotTran5J"],
            "count": row["zTotTran"],
        }
        for row in response
    ]


def get_symbol_notifications(symbol_id: str) -> list[dict]:
    response = requests.get(
        url="http://tsetmc.ir/tsev2/data/CodalTopNew.aspx",
        params={
            "i": symbol_id,
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    data = ast.literal_eval(response)

    notifications = [{"title": row[3], "datetime": jdatetime.strptime(row[4], "%y/%m/%d %H:%M")} for row in data]

    return notifications


def get_symbol_state_changes(symbol_id: str) -> list[dict]:
    response = requests.get(
        url=" http://tsetmc.ir/Loader.aspx",
        params={
            "i": symbol_id,
            "Partree": "15131L",
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    data = BeautifulSoup(response, "lxml")

    state_changes = []
    trs = data.find("tbody").find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        state_changes.append({"datetime": jdatetime.strptime(f"{tds[0].text} {tds[1].text}", "%Y/%m/%d %H:%M:%S"), "new_state": tds[2].text.strip()})

    return state_changes


def get_symbol_id_details(symbol_id: str) -> dict:
    response = requests.get(
        url="http://tsetmc.ir/Loader.aspx",
        params={
            "i": symbol_id,
            "Partree": "15131M",
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    data = BeautifulSoup(response, "lxml")

    trs = data.find_all("tr")
    values = {}
    for tr in trs:
        tds = tr.find_all("td")
        values[tds[0].contents[0]] = str(tds[1].contents[0]).strip()

    result = {
        "isin": values.get("کد 12 رقمی نماد"),
        "short_isin": values.get("کد 5 رقمی نماد"),
        "short_name": values.get("نماد فارسی"),
        "long_name": values.get("نماد 30 رقمی فارسی"),
        "english_name": values.get("نام لاتین شرکت"),
        "company_isin": values.get("کد 12 رقمی شرکت"),
        "company_short_isin": values.get("کد 4 رقمی شرکت"),
        "company_name": values.get("نام شرکت"),
        "market_code": values.get("کد تابلو"),
        "market_name": values.get("بازار"),
        "group_code": values.get("کد گروه صنعت"),
        "group_name": values.get("گروه صنعت"),
        "subgroup_code": values.get("کد زیر گروه صنعت"),
        "subgroup_name": values.get("زیر گروه صنعت"),
    }

    return result


def get_symbol_traders_type_history(symbol_id: str) -> list[dict]:
    response = requests.get(
        url="http://tsetmc.ir/tsev2/data/clienttype.aspx",
        params={
            "i": symbol_id,
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    traders_type_history = []
    raw_data = response.split(";")
    for row in raw_data:
        (dt, r_buy_c, l_buy_c, r_sell_c, l_sell_c, r_buy_v, l_buy_v, r_sell_v, l_sell_v, r_buy_vl, l_buy_vl, r_sell_vl, l_sell_vl) = row.split(",")
        traders_type_history.append(
            {
                "date": jdate.fromgregorian(
                    year=int(dt[:4]),
                    month=int(dt[4:6]),
                    day=int(dt[6:]),
                ),
                "legal": {
                    "buy": {
                        "value": l_buy_vl,
                        "volume": l_buy_v,
                        "count": l_buy_c,
                    },
                    "sell": {
                        "value": l_sell_vl,
                        "volume": l_sell_v,
                        "count": l_sell_c,
                    },
                },
                "real": {
                    "buy": {
                        "value": r_buy_vl,
                        "volume": r_buy_v,
                        "count": r_buy_c,
                    },
                    "sell": {
                        "value": r_sell_vl,
                        "volume": r_sell_v,
                        "count": r_sell_c,
                    },
                },
            }
        )

    return traders_type_history


def get_symbol_shareholders(company_isin: str) -> list[dict]:
    response = requests.get(
        url="http://tsetmc.ir/Loader.aspx",
        params={
            "c": company_isin,
            "Partree": "15131T",
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    soup = BeautifulSoup(response, "lxml")

    shareholders = []
    trs = soup.find_all("tr", {"class": "sh"})
    for tr in trs:
        tds = tr.find_all("td")

        shareholder_id = tr["onclick"]
        shareholder_id = shareholder_id[shareholder_id.index("'") + 1 : shareholder_id.index(",")]
        name = tds[0].text.strip()
        count = int(tds[1].div["title"].replace(",", ""))
        percentage = float(tds[2].text)
        change = locale.atoi(tds[3].text.strip())

        shareholders.append(
            {
                "id": shareholder_id,
                "name": name,
                "count": count,
                "percentage": percentage,
                "change": change,
            }
        )

    return shareholders


def get_symbol_shareholder_details(shareholder_id: str, company_isin: str):
    response = requests.get(
        url=f"http://www.tsetmc.com/tsev2/data/ShareHolder.aspx?i={shareholder_id}%2C{company_isin}",
        params={
            "i": f"{shareholder_id}%C{company_isin}",
        },
        headers=get_request_headers(),
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    response = response.text

    response = response.split(";")

    chart = []
    portfolio = []
    for row in response:
        row = row.split(",")
        if len(row) == 2:
            chart.append(
                {
                    "date": convert_deven_to_jdate(deven=int(row[0])),
                    "count": int(row[1]),
                }
            )
        elif len(row) == 4:
            portfolio.append(
                {
                    "symbol_id": row[0][1:] if "#" in row[0] else row[0],
                    "long_name": row[1],
                    "count": int(row[2]),
                    "percentage": float(row[3]),
                }
            )

    return {
        "chart": chart,
        "portfolio": portfolio,
    }
