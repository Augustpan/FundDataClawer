# -*- coding: UTF-8 -*-

import pandas

def clean_up(fund_id):
    aa = pandas.read_csv("save/AssetAllocation_{}.csv".format(fund_id))
    bh = pandas.read_csv("save/BondHolding_{}.csv".format(fund_id))
    nav = pandas.read_csv("save/NetAssetValue_{}.csv".format(fund_id))
    fr = pandas.read_csv("save/Rating_{}.csv".format(fund_id))
    sa = pandas.read_csv("save/SectorAllocation_{}.csv".format(fund_id))
    sh = pandas.read_csv("save/StockHolding_{}.csv".format(fund_id))
    tr = pandas.read_csv("save/TurnoverRate_{}.csv".format(fund_id))
    hs = pandas.read_csv("save/HolderStructure_{}.csv".format(fund_id))

    aa.columns = ["report_date", "stock_proportion", "bond_proportion", "cash_proportion", "net_asset"]
    aa.stock_proportion = list(map(lambda x: float(x.split("%")[0]), aa.stock_proportion))
    aa.bond_proportion = list(map(lambda x: float(x.split("%")[0]), aa.bond_proportion))
    aa.cash_proportion = list(map(lambda x: float(x.split("%")[0]), aa.cash_proportion))
    aa.to_csv("clean/AssetAllocation_{}.csv".format(fund_id), index=0)

    bh = bh.drop(["序号"], axis=1)
    bh.columns = ["bond_id", "bond_name", "proportion", "market_value", "quarter", "report_date"]
    bh.proportion = list(map(lambda x: float(x.split("%")[0]), bh.proportion))
    bh.quarter = list(map(lambda x: "{}-{}".format(x.split("年")[0], x.split("年")[1][0]), bh.quarter))
    bh.to_csv("clean/BondHolding_{}.csv".format(fund_id), index=0)

    nav = nav.drop(["SDATE", "ACTUALSYI", "NAVTYPE", "FHFCBZ", "DTYPE", "FHSP"], axis=1)
    nav.columns = ["report_date", "unit_net_value", "accumulated_net_value", "growth_rate", "subscription_status", "redemption_status", "bonus_per_share"]
    nav.to_csv("clean/NetAssetValue_{}.csv".format(fund_id), index=0)

    fr = fr.drop(["FCODE", "HTPJ"], axis=1)
    fr.columns = ["report_date", "ZSPJ", "SZPJ3", "SZPJ5", "JAPJ"]
    fr.to_csv("clean/Rating_{}.csv".format(fund_id), index=0)

    sa["quarter"] = list(map(lambda x: "{}-{}".format(x[0], x[1]), zip(sa.Year, sa.Quarter)))
    sa = sa.drop(["BZDM", "SZDesc", "ZJZBLDesc", "SAMMVPCTNV", "PCTCP", "SHORTNAME", "ABBNAME", "JJGSID", "FTYPE", "FUNDTYP", "FEATURE", "Year", "Quarter"], axis=1)
    sa.columns = ["report_date", "sector_code", "sector_name", "market_value", "proportion", "date", "quarter"]
    sa.to_csv("clean/SectorAllocation_{}.csv".format(fund_id), index=0)

    sh["quarter"] = list(map(lambda x: "{}-{}".format(x.split("年")[0], x.split("年")[1][0]), sh.Quarter))
    sh = sh.drop(["序号", "最新价", "涨跌幅", "相关资讯", "Quarter"], axis=1)
    sh.columns = ["stock_id", "stock_name", "proportion", "share", "market_value", "report_date", "quarter"]
    sh.proportion = list(map(lambda x: float(x.split("%")[0]), sh.proportion))
    sh.market_value = list(map(lambda x: x.replace(",", ""), sh.market_value))
    sh.to_csv("clean/StockHolding_{}.csv".format(fund_id), index=0)

    tr.columns = ["report_date", "turnover_rate"]
    tr.to_csv("clean/TurnoverRate_{}.csv".format(fund_id), index=0)

    hs.columns = ["report_date", "institutional_proportion", "individual_proportion", "internal_proportion", "total_share"]
    hs.to_csv("clean/HolderStructure_{}.csv".format(fund_id))