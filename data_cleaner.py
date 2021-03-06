# -*- coding: UTF-8 -*-

import pandas

def removePercentSign(col):
    def proc(x):
        x = x.split("%")[0]
        if x == "---":
            return
        else: 
            return float(x)
    return list(map(proc, col))

def removeComma(col):
    def proc(x):
        try:
            x = x.replace(",", "")
        except AttributeError:
            # x is float
            return x
        if x == "---":
            return
        else:
            return x
    return list(map(proc, col))

def dateToQuarter(col):
    def proc(x):
        sp = x.split("-")
        year = sp[0]
        quarter_map = {"01":1, "02":1, "03":1, 
                       "04":2, "05":2, "06":2,
                       "07":3, "08":3, "09":3,
                       "10":4, "11":4, "12":4}
        quarter = "{}-{}".format(year, quarter_map[sp[1]])
        return quarter
    return list(map(proc, col))

def cleanAssetAllocation(fund_id):
    try:
        aa = pandas.read_csv("raw/AssetAllocation_{}.csv".format(fund_id))
        new_aa = pandas.DataFrame()
        new_aa["net_asset"] =  removeComma(aa["净资产（亿元）"])
        new_aa["stock_proportion"] = removePercentSign(aa["股票占净比"])
        new_aa["cash_proportion"] = removePercentSign(aa["现金占净比"])
        if "债券占净比" in aa.columns:
            new_aa["bond_proportion"] = removePercentSign(aa["债券占净比"])
        else:
            new_aa["bond_proportion"] = None
        if "存托凭证占净比" in aa.columns:
            new_aa["deposit_proportion"] = removePercentSign(aa["存托凭证占净比"])
        else:
            new_aa["deposit_proportion"] = None
        new_aa["report_date"] = aa["报告期"]
        new_aa["quarter"] = dateToQuarter(aa["报告期"])
        new_aa.to_csv("clean/AssetAllocation_{}.csv".format(fund_id), index=0)
        return new_aa
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanNetAssetValue(fund_id):
    try:
        nav = pandas.read_csv("raw/NetAssetValue_{}.csv".format(fund_id))
        nav = nav.drop(["SDATE", "ACTUALSYI", "NAVTYPE", "FHFCBZ", "DTYPE", "FHSP"], axis=1)
        nav.columns = ["report_date", "unit_net_value", "accumulated_net_value", "growth_rate", "subscription_status", "redemption_status", "bonus_per_share"]
        nav["quarter"] = dateToQuarter(nav.report_date)
        nav.to_csv("clean/NetAssetValue_{}.csv".format(fund_id), index=0)
        return nav
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanBondHoldings(fund_id):
    try:
        bh = pandas.read_csv("raw/BondHolding_{}.csv".format(fund_id))
        bh = bh.drop(["序号"], axis=1)
        bh.columns = ["bond_id", "bond_name", "proportion", "market_value", "quarter", "report_date"]
        bh.proportion = removePercentSign(bh.proportion)
        bh.quarter = list(map(lambda x: "{}-{}".format(x.split("年")[0], x.split("年")[1][0]), bh.quarter))
        bh.market_value = removeComma(bh.market_value)
        bh.to_csv("clean/BondHolding_{}.csv".format(fund_id), index=0)
        return bh
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanFundRating(fund_id):
    try:
        fr = pandas.read_csv("raw/FundRating_{}.csv".format(fund_id))
        fr = fr.drop(["FCODE", "HTPJ"], axis=1)
        fr.columns = ["report_date", "ZSPJ", "SZPJ3", "SZPJ5", "JAPJ"]
        fr.to_csv("clean/FundRating_{}.csv".format(fund_id), index=0)
        return fr
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanSectorAllocation(fund_id):
    try:
        sa = pandas.read_csv("raw/SectorAllocation_{}.csv".format(fund_id))
        sa["quarter"] = list(map(lambda x: "{}-{}".format(x[0], x[1]), zip(sa.Year, sa.Quarter)))
        sa = sa.drop(["BZDM", "SZDesc", "ZJZBLDesc", "SAMMVPCTNV", "PCTCP", "SHORTNAME", "ABBNAME", "JJGSID", "FTYPE", "FUNDTYP", "FEATURE", "Year", "Quarter", "Date"], axis=1)
        sa.columns = ["report_date", "sector_code", "sector_name", "market_value", "proportion", "quarter"]
        sa.to_csv("clean/SectorAllocation_{}.csv".format(fund_id), index=0)
        return sa
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanStockHoldings(fund_id):
    try:
        sh = pandas.read_csv("raw/StockHolding_{}.csv".format(fund_id))
        sh["quarter"] = list(map(lambda x: "{}-{}".format(x.split("年")[0], x.split("年")[1][0]), sh.Quarter))
        sh = sh.drop(["序号", "最新价", "涨跌幅", "相关资讯", "Quarter"], axis=1)
        sh.columns = ["stock_id", "stock_name", "proportion", "share", "market_value", "report_date", "quarter"]
        sh.proportion = removePercentSign(sh.proportion)
        sh.share = removeComma(sh.share)
        sh.market_value = removeComma(sh.market_value)
        sh.to_csv("clean/StockHolding_{}.csv".format(fund_id), index=0)
        return sh
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanTurnoverRate(fund_id):
    try:
        tr = pandas.read_csv("raw/TurnoverRate_{}.csv".format(fund_id))
        tr.columns = ["report_date", "turnover_rate"]
        tr.to_csv("clean/TurnoverRate_{}.csv".format(fund_id), index=0)
        tr["quarter"] = dateToQuarter(tr.report_date)
        return tr
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanHolderStructure(fund_id):
    try:
        hs = pandas.read_csv("raw/HolderStructure_{}.csv".format(fund_id))
        hs.columns = ["report_date", "institutional_proportion", "individual_proportion", "internal_proportion", "total_share"]
        hs.institutional_proportion = removePercentSign(hs.institutional_proportion)
        hs.individual_proportion = removePercentSign(hs.individual_proportion)
        hs.internal_proportion = removePercentSign(hs.internal_proportion)
        hs["quarter"] = dateToQuarter(hs.report_date)
        hs.total_share = removeComma(hs.total_share)
        hs.to_csv("clean/HolderStructure_{}.csv".format(fund_id), index=0)
        return hs
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def cleanFundManager(fund_id):
    try:
        fm = pandas.read_csv("raw/FundManager_{}.csv".format(fund_id))
        fm = fm.drop(["任职期间"], axis=1)
        fm.columns = ["start_date", "expiry_date", "manager_name", "return_rate"]
        fm.return_rate = removePercentSign(fm.return_rate)
        fm.to_csv("clean/FundManager_{}.csv".format(fund_id), index=0)
        return fm
    except pandas.errors.EmptyDataError:
        # TODO: hanlde empty file
        pass

def exportToExcel(fund_id, list_df):
    with pandas.ExcelWriter("excel_export/{}.xlsx".format(fund_id)) as writer:
        for name, df in list_df:
            try:
                df.to_excel(writer, name, index=0)
            except AttributeError:
                pass