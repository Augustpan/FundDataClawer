# FundDataClawer

## 1. Raw dataset
### NetAssetValue
- FSRQ：净值日期
- DWJZ：单位净值（元）
- LJJZ：累计净值（元）
- SDATE：？？
- ACTUALSYI：？？
- NAVTYPE：？？
- JZZZL：日增长率，%
- SGZT：申购状态
- SHZT：赎回状态
- FHFCZ：每份红利，元
- FHFCBZ：？？
- DTYPE：空
- FHSP：分红送配

### Rating
- FCODE：基金代码
- RDATE：评级日期
- HTPJ：？？
- ZSPJ：招商评级
- SZPJ3：上海证券评级3年期
- SZPJ5：上海证券评级5年期
- JAPJ：济安金信评级

### SectorAllocation
- BZDM：基金代码
- FSRQ：报告日期
- HYDM：证监会行业代码
- HYMC：行业名称
- SZ：市值，万元
- SZDesc：市值，万元（加逗号）
- ZJZBL：占净值比例，%
- ZJZBLDesc：占净值比例，%（加百分号）
- SAMMVPCTNV：？？
- PCTCP：？？
- SHORTNAME：基金简称
- ABBNAME：基金英语简称
- JJGSID：？？
- FTYPE：基金类型
- FUNDTYP：空
- FEATURE：？？
- Quarter：季度
- Date：报告日期

### TurnoverRate
- REPORTDATE：报告日期
- STOCKTURNOVER：转手率，%


## 2. Clean dataset

| FILE             | VARIABLE                 | DESCRIPTION                          |
| ---------------- | ------------------------ | ------------------------------------ |
| AssetAllocation  | report_date              | 报告日期                         |
|                  | stock_proportion         | 股票占净值比例（%）         |
|                  | bond_proportion          | 债券占净值比例（%）         |
|                  | cash_proportion          | 现金占净值比例（%）         |
|                  | net_asset                | 净资产（亿元）                |
| BondHolding      | bond_id                  | 债券代码                         |
|                  | bond_name                | 债券名称                         |
|                  | proportion               | 占净值比例（%）               |
|                  | market_value             | 仓持市值（万元）             |
|                  | quarter                  | 报告季度                         |
|                  | report_date              | 报告日期                         |
| HolderStructure  | report_date              | 报告日期                         |
|                  | institutional_proportion | 机构持有比例（%）            |
|                  | individual_proportion    | 个人持有比例（%）            |
|                  | internal_proportion      | 内部持有比例（%）            |
|                  | total_share              | 总份额（亿份）                |
| NetAssetValue    | report_date              | 报告日期                         |
|                  | unit_net_value           | 单位净值（元）                |
|                  | accumulated_net_value    | 累计净值（元）                |
|                  | growth_rate              | 日增长率（%）                  |
|                  | subscription_status      | 申购状态（暂停申购/开放申购/封闭期） |
|                  | redemption_status        | 赎回状态（暂停赎回/开放赎回/封闭期） |
|                  | bonus_per_share          | 每份红利（元）                |
| Rating           | report_date              | 报告日期                         |
|                  | ZSPJ                     | 招商评级                         |
|                  | SZPJ3                    | 上证评级3年期                  |
|                  | SZPJ5                    | 上证评级5年期                  |
|                  | JAPJ                     | 济安金信评级                   |
| SectorAllocation | report_date              | 报告日期                         |
|                  | sector_code              | 行业代码                         |
|                  | sector_name              | 行业名称                         |
|                  | market_value             | 市值（万元）                   |
|                  | proportion               | 占净值比例（%）               |
|                  | quarter                  | 报告季度                         |
| StockHolding     | stock_id                 | 股票代码                         |
|                  | stock_name               | 股票名称                         |
|                  | proportion               | 占净值比例（%）               |
|                  | share                    | 持股数（万股）                |
|                  | market_value             | 仓持市值（万元）             |
|                  | report_date              | 报告日期                         |
|                  | quarter                  | 报告季度                         |
| TurnoverRate     | report_date              | 报告日期                         |
|                  | turnover_rate            | 换手率（%）                     |