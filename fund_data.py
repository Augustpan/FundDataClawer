# -*- coding: UTF-8 -*-

import requests
import re
import json
import pandas
from bs4 import BeautifulSoup

# utility function for parsing return values from host http://fundf10.eastmoney.com/FundArchivesDatas.aspx
def parseFundArchivesDatasReturn(r):
    # TODO: check status code, handle exceptions

    # the return value is a JS expression, we extract the JSON string in it
    m = re.match("var\s+\w+\s*=\s*(\{.+\})\s*;", r.text)
    # TODO: handle exceptions

    # convert JS style JSON string into Python style
    json_str = m.group(1) \
        .replace("arryear", "\"arryear\"") \
        .replace("curyear", "\"curyear\"") \
        .replace("content", "\"content\"")

    return json.loads(json_str)

# parse html <table> tag into pandas DataFrame
def parseHTMLTable(tag_table):
    parsed_list = []

    col_names = []
    for th in tag_table.select("thead > tr > th"):
        col_names.append(th.get_text())

    for tr in tag_table.select("tbody > tr"):
        dict_row = {}
        for ind, td in enumerate(tr.select("td")):
            dict_row[col_names[ind]] = td.get_text()
        parsed_list.append(dict_row)
    
    return pandas.DataFrame(parsed_list)

def retrieveFundNetAssetValue(fund_id):
    api_host = "https://api.fund.eastmoney.com/f10/lsjz"

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Host': 'api.fund.eastmoney.com',
        'Referer':'http://fundf10.eastmoney.com/'
    }

    r = requests.get("{}?callback=&fundCode={}&pageIndex=1&pageSize=20&startDate=&endDate=".format(api_host, fund_id), headers=headers)
    
    # TODO: handle exceptions
    ret = json.loads(r.text)
    total_page = ret["TotalCount"] // 20
    if total_page * 20 < ret["TotalCount"]:
        total_page += 1

    # TODO: handle exceptions
    df_return = pandas.DataFrame(ret["Data"]["LSJZList"])

    for page in range(2, total_page+1):
        r = requests.get("{}?callback=&fundCode={}&pageIndex={}&pageSize=20&startDate=&endDate=".format(api_host, fund_id, page), headers=headers)
        ret = json.loads(r.text)

        # TODO: handle exceptions
        df_return = pandas.concat([df_return, pandas.DataFrame(ret["Data"]["LSJZList"])])
    
    return df_return

def retrieveFundRating(fund_id):
    api_host = "http://api.fund.eastmoney.com/F10/JJPJ/"

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Host': 'api.fund.eastmoney.com',
        'Referer':'http://fundf10.eastmoney.com/'
    }

    r = requests.get("{}?callback=&fundcode={}&pageIndex=1&pageSize=50".format(api_host, fund_id), headers=headers)
    
    # TODO: handle exceptions
    ret = json.loads(r.text)
    total_page = ret["TotalCount"] // 50
    if total_page * 50 < ret["TotalCount"]:
        total_page += 1
    
    # TODO: handle exceptions
    df_return = pandas.DataFrame(ret["Data"])

    for page in range(2, total_page+1):
        r = requests.get("{}?callback=&fundCode={}&pageIndex={}&pageSize=50".format(api_host, fund_id, page), headers=headers)
        ret = json.loads(r.text)

        # TODO: handle exceptions
        df_return = pandas.concat([df_return, pandas.DataFrame(ret["Data"])])
    
    return df_return

def retrieveFundAssetAllocation(fund_id):
    r = requests.get("http://fundf10.eastmoney.com/zcpz_{}.html".format(fund_id))
    
    # TODO: handle exceptions
    soup = BeautifulSoup(r.text, "lxml")
    tag_table = soup.select_one("div.box > div.boxitem > table")
    df = parseHTMLTable(tag_table)

    return df

def retrieveFundSectorAllocation(fund_id):
    api_host = "http://api.fund.eastmoney.com/f10/HYPZ/"
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Host': 'api.fund.eastmoney.com',
        'Referer':'http://fundf10.eastmoney.com/'
    }

    r = requests.get("{}?fundCode={}&year=&callback=".format(api_host, fund_id), headers=headers)

    # TODO: handle exceptions
    ret = json.loads(r.text)
    
    df_return = pandas.DataFrame()

    listyear = ret["Data"]["ListYears"]
    for year in listyear:
        r = requests.get("{}?fundCode={}&year={}&callback=".format(api_host, fund_id, year), headers=headers)
        
        # TODO: handle exceptions
        ret = json.loads(r.text)
        for QuarterInfos in ret["Data"]["QuarterInfos"]:
            quarter = QuarterInfos["Quarter"]
            date = QuarterInfos["JZRQ"]
            df = pandas.DataFrame(QuarterInfos["HYPZInfo"])
            df["Quarter"] = quarter
            df["Date"] = date
            df["Year"] = year
            df_return = pandas.concat([df_return, df])
    
    return df_return

def retrieveFundBondHoldings(fund_id):
    api_host = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"

    r = requests.get("{}?type=zqcc&code={}&year=".format(api_host, fund_id))
    ret = parseFundArchivesDatasReturn(r)

    df_return = pandas.DataFrame()

    arryear = ret["arryear"]
    for year in arryear:
        r = requests.get("{}?type=zqcc&code={}&year={}".format(api_host, fund_id, year))
        ret = parseFundArchivesDatasReturn(r)
        
        soup = BeautifulSoup(ret["content"], "lxml")
        boxes = soup.select("div.box")
        for box in boxes:
            df = parseHTMLTable(box.select_one("table"))
            title = box.select_one("h4").get_text()
            sp = title.split()
            quarter = sp[1]
            date = sp[3]
            m = re.match("\D+(\d+-\d+-\d+)", date)
            df["Quarter"] = quarter
            df["Date"] = m.group(1)
            df_return = pandas.concat([df_return, df])
    
    return df_return

def retrieveFundStockHoldings(fund_id):
    api_host = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"

    r = requests.get("{}?type=jjcc&code={}&topline=10&year=&month=".format(api_host, fund_id))
    ret = parseFundArchivesDatasReturn(r)
    
    df_return = pandas.DataFrame()

    arryear = ret["arryear"]
    for year in arryear:
        r = requests.get("{}?type=jjcc&code={}&topline=10&year={}&month=".format(api_host, fund_id, year))
        ret = parseFundArchivesDatasReturn(r)
        soup = BeautifulSoup(ret["content"], "lxml")
        month = []
        btns_loadmore = soup.select("div.tfoot > font > a")
        for btn in btns_loadmore:
            month.append(btn["onclick"].split(",")[1].strip())
        month = ",".join(month)
        
        r = requests.get("{}?type=jjcc&code={}&topline=10&year={}&month={}".format(api_host, fund_id, year, month))
        ret = parseFundArchivesDatasReturn(r)
        
        soup = BeautifulSoup(ret["content"], "lxml")
        boxes = soup.select("div.box")
        for box in boxes:
            df = parseHTMLTable(box.select_one("table"))
            title = box.select_one("h4").get_text()
            sp = title.split()
            quarter = sp[1]
            date = sp[3]
            m = re.match("\D+(\d+-\d+-\d+)", date)
            df["Quarter"] = quarter
            df["Date"] = m.group(1)
            df_return = pandas.concat([df_return, df])

    return df_return

def retrieveFundTurnoverRate(fund_id):
    api_host = "http://api.fund.eastmoney.com/f10/JJHSL/"

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Host': 'api.fund.eastmoney.com',
        'Referer':'http://fundf10.eastmoney.com/'
    }

    r = requests.get("{}?callback=&fundcode={}&pageIndex=1&pageSize=20".format(api_host, fund_id), headers=headers)
    
    # TODO: handle exceptions
    ret = json.loads(r.text)
    total_page = ret["TotalCount"] // 20
    if total_page * 20 < ret["TotalCount"]:
        total_page += 1
    
    # TODO: handle exceptions
    df_return = pandas.DataFrame(ret["Data"])

    for page in range(2, total_page+1):
        r = requests.get("{}?callback=&fundCode={}&pageIndex={}&pageSize=20".format(api_host, fund_id, page), headers=headers)
        ret = json.loads(r.text)

        # TODO: handle exceptions
        df_return = pandas.concat([df_return, pandas.DataFrame(ret["Data"])])
    
    return df_return

# 基金代码
fund_id = 110012

# 基金净值
retrieveFundNetAssetValue(fund_id).to_csv("NetAssetValue_{}.csv".format(fund_id), index=0)
# 基金评级
retrieveFundRating(fund_id).to_csv("Rating_{}.csv".format(fund_id), index=0)
# 换手率
retrieveFundTurnoverRate(fund_id).to_csv("TurnoverRate_{}.csv".format(fund_id), index=0)
# 资产配置
retrieveFundAssetAllocation(fund_id).to_csv("AssetAllocation_{}.csv".format(fund_id), index=0)
# 行业配置
retrieveFundSectorAllocation(fund_id).to_csv("SectorConfig_{}.csv".format(fund_id), index=0)
# 股票仓持
retrieveFundStockHoldings(fund_id).to_csv("StockHolding_{}.csv".format(fund_id), index=0)
# 债券仓持
retrieveFundBondHoldings(fund_id).to_csv("BondHolding_{}.csv".format(fund_id), index=0)