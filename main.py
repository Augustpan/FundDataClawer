# -*- coding: UTF-8 -*-

from data_clawer import *
from data_cleaner import *
from db_manager import *

def retrieveAllAndSave(fund_id):
    retrieveFundNetAssetValue(fund_id).to_csv("raw/NetAssetValue_{}.csv".format(fund_id), index=0)
    retrieveFundRating(fund_id).to_csv("raw/FundRating_{}.csv".format(fund_id), index=0)
    retrieveFundHolderStructure(fund_id).to_csv("raw/HolderStructure_{}.csv".format(fund_id), index=0)
    retrieveFundTurnoverRate(fund_id).to_csv("raw/TurnoverRate_{}.csv".format(fund_id), index=0)
    retrieveFundAssetAllocation(fund_id).to_csv("raw/AssetAllocation_{}.csv".format(fund_id), index=0)
    retrieveFundSectorAllocation(fund_id).to_csv("raw/SectorAllocation_{}.csv".format(fund_id), index=0)
    retrieveFundStockHoldings(fund_id).to_csv("raw/StockHolding_{}.csv".format(fund_id), index=0)
    retrieveFundBondHoldings(fund_id).to_csv("raw/BondHolding_{}.csv".format(fund_id), index=0)
    retrieveFundManagerInfo(fund_id).to_csv("raw/FundManager_{}.csv".format(fund_id), index=0)

def cleanAllAndSave(fund_id):
    list_df = [
        ("AssetAllocation", cleanAssetAllocation(fund_id)),
        ("NetAssetValue", cleanNetAssetValue(fund_id)),
        ("FundManager", cleanFundManager(fund_id)),
        ("HolderStructure", cleanHolderStructure(fund_id)),
        ("TurnoverRate", cleanTurnoverRate(fund_id)),
        ("StockHoldings", cleanStockHoldings(fund_id)),
        ("SectorAllocation", cleanSectorAllocation(fund_id)),
        ("FundRating", cleanFundRating(fund_id)),
        ("BondHoldings", cleanBondHoldings(fund_id)),
    ]
    exportToExcel(fund_id, list_df)

# TODO: synchronize fund manager data to database
def saveAllToDatabase(fund_id):
    updateAssetAllocation(fund_id)
    updateNetAssetValue(fund_id)
    updateHolderStructure(fund_id)
    updateFundRating(fund_id) 
    updateBondHoldings(fund_id)
    updateStockHoldings(fund_id)
    updateSectorAllocation(fund_id)

fund_id_list = [
    "001938","110011","110012","519697","952004","007119",
    "002146","002147","161017","163407","206018","004614",
    "000032","486002","003474","110001","519732","001875",
    "166002","001500","000362","270002","260108"
]

for ind, fund_id in enumerate(fund_id_list):
    print("{} of {}".format(ind+1, len(fund_id_list)))
    print("fund_id: {}".format(fund_id))
    retrieveAllAndSave(fund_id)
    cleanAllAndSave(fund_id)
    saveAllToDatabase(fund_id)