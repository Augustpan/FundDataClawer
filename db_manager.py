# -*- coding: UTF-8 -*-

import pandas
import mysql.connector
import re

def updateAssetAllocation(fund_id):
    try:
        aa = pandas.read_csv("clean/AssetAllocation_{}.csv".format(fund_id))
    except FileNotFoundError:
        return
    
    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in aa.iterrows():
        fields = "REPORT_DATE,FUND_ID"
        values = "'{}','{}'".format(row.report_date, fund_id) 
        if not pandas.isna(row.stock_proportion):
            fields = "{},{}".format(fields, "STOCK_PROP")
            values = "{},{}".format(values, row.stock_proportion)
        if not pandas.isna(row.bond_proportion):
            fields = "{},{}".format(fields, "BOND_PROP")
            values = "{},{}".format(values, row.bond_proportion)
        if not pandas.isna(row.cash_proportion):
            fields = "{},{}".format(fields, "CASH_PROP")
            values = "{},{}".format(values, row.cash_proportion)
        if not pandas.isna(row.cash_proportion):
            fields = "{},{}".format(fields, "NET_ASSET_VALUE")
            values = "{},{}".format(values, row.net_asset)
        try:
            mycursor.execute("INSERT INTO ASSET_ALLOCATION ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass

    mycursor.close()
    mydb.close()

def updateNetAssetValue(fund_id):
    try:
        nav = pandas.read_csv("clean/NetAssetValue_{}.csv".format(fund_id))
    except FileNotFoundError:
        return

    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in nav.iterrows():
        fields = "REPORT_DATE,FUND_ID,UNIT_NET_VALUE"
        values = "'{}','{}',{}".format(
            row.report_date, 
            fund_id,
            row.unit_net_value
        )
        if not pandas.isna(row.accumulated_net_value):
            fields = "{},{}".format(fields, "ACCU_NET_VALUE")
            values = "{},{}".format(values, row.accumulated_net_value)
        fields = "{},{},{}".format(fields, "SUBSCRIPTION", "REDEMPTION")
        values = "{},'{}','{}'".format(values, row.subscription_status, row.redemption_status)
        if not pandas.isna(row.bonus_per_share):
            fields = "{},{}".format(fields, "BONUS_PER_SHARE")
            values = "{},{}".format(values, row.bonus_per_share)
        try:
            mycursor.execute("INSERT INTO DAILY_NET_VALUE ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass

    mycursor.close()
    mydb.close()

def updateHolderStructure(fund_id):
    try:
        hs = pandas.read_csv("clean/HolderStructure_{}.csv".format(fund_id))
    except FileNotFoundError:
        return
    
    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in hs.iterrows():
        fields = "REPORT_DATE,FUND_ID"
        values = "'{}','{}'".format(
            row.report_date, 
            fund_id
        )
        if not pandas.isna(row.institutional_proportion):
            fields = "{},{}".format(fields, "INST_PROP")
            values = "{},{}".format(values, row.institutional_proportion)
        if not pandas.isna(row.individual_proportion):
            fields = "{},{}".format(fields, "INDI_PROP")
            values = "{},{}".format(values, row.individual_proportion)
        if not pandas.isna(row.internal_proportion):
            fields = "{},{}".format(fields, "INTE_PROP")
            values = "{},{}".format(values, row.internal_proportion)
        if not pandas.isna(row.total_share):
            fields = "{},{}".format(fields, "TOTAL_SHARE")
            values = "{},{}".format(values, row.total_share)
        try:
            mycursor.execute("INSERT INTO HOLDER_STRUCTURE ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass

    mycursor.close()
    mydb.close()

def updateFundRating(fund_id):
    try:
        fr = pandas.read_csv("clean/FundRating_{}.csv".format(fund_id))
    except FileNotFoundError:
        return
    
    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in fr.iterrows():
        fields = "REPORT_DATE,FUND_ID"
        values = "'{}','{}'".format(
            row.report_date, 
            fund_id
        )
        if not pandas.isna(row.ZSPJ):
            fields = "{},{}".format(fields, "ZSPJ")
            values = "{},{}".format(values, row.ZSPJ)
        if not pandas.isna(row.SZPJ3):
            fields = "{},{}".format(fields, "SZPJ3")
            values = "{},{}".format(values, row.SZPJ3)
        if not pandas.isna(row.SZPJ5):
            fields = "{},{}".format(fields, "SZPJ5")
            values = "{},{}".format(values, row.SZPJ3)
        if not pandas.isna(row.JAPJ):
            fields = "{},{}".format(fields, "JAPJ")
            values = "{},{}".format(values, row.JAPJ)
        try:
            mycursor.execute("INSERT INTO FUND_RATING ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass

    mycursor.close()
    mydb.close()

def updateBondHoldings(fund_id):
    try:
        bh = pandas.read_csv("clean/BondHolding_{}.csv".format(fund_id))
    except FileNotFoundError:
        return

    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in bh.iterrows():
        fields = "REPORT_DATE,FUND_ID,BOND_ID,BOND_NAME,BOND_SPEC_PROP,BOND_SPEC_VALUE"
        values = "'{}','{}','{}','{}',{},{}".format(
            row.report_date, 
            fund_id,
            row.bond_id,
            row.bond_name,
            row.proportion,
            row.market_value
        )
        try:
            mycursor.execute("INSERT INTO BOND_HOLDINGS ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass

    mycursor.close()
    mydb.close()

def updateStockHoldings(fund_id):
    try:
        sh = pandas.read_csv("clean/StockHolding_{}.csv".format(fund_id))
    except FileNotFoundError:
        return

    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in sh.iterrows():
        fields = "REPORT_DATE,FUND_ID,STOCK_ID,STOCK_NAME"
        values = "'{}','{}','{}','{}'".format(
            row.report_date, 
            fund_id,
            row.stock_id,
            row.stock_name
        )
        if not pandas.isna(row.proportion):
            fields = "{},{}".format(fields, "STOCK_SPEC_PROP")
            values = "{},{}".format(values, row.proportion)
        fields = "{},{}".format(fields, "STOCK_SPEC_SHARE")
        values = "{},{}".format(values, row.share)
        if not pandas.isna(row.market_value):
            fields = "{},{}".format(fields, "STOCK_SPEC_VALUE")
            values = "{},{}".format(values, row.market_value)
        try:
            mycursor.execute("INSERT INTO STOCK_HOLDINGS ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass
        except:
            print(values)

    mycursor.close()
    mydb.close()

def updateSectorAllocation(fund_id):
    try:
        sa = pandas.read_csv("clean/SectorAllocation_{}.csv".format(fund_id))
    except FileNotFoundError:
        return

    # user@host:passwd
    with open("mysql.config") as f:
        config = f.read()
    user, host, passwd = re.split("[@:]", config)

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database='FUNDDATA',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    for _, row in sa.iterrows():
        fields = "REPORT_DATE,FUND_ID,SECTOR_CODE,SECTOR_NAME,SECTOR_ASSET_VALUE"
        values = "'{}','{}','{}','{}',{}".format(
            row.report_date, 
            fund_id,
            row.sector_code,
            row.sector_name, 
            row.market_value
        )
        if not pandas.isna(row.proportion):
            fields = "{},{}".format(fields, "SECTOR_PROP")
            values = "{},{}".format(values, row.proportion)
        try:
            mycursor.execute("INSERT INTO SECTOR_ALLOCATION ({}) VALUES ({})".format(fields, values))
            mydb.commit()
        except mysql.connector.errors.IntegrityError:
            # record existed
            pass

    mycursor.close()
    mydb.close()
