# [China-A-Sort](https://github.com/mlfina/China-A-Sort)

## Download Data

1. Value-Weighted Sorted Portfolios

    - [univariate-sorted long-short factor](https://github.com/mlfina/China-A-Sort/blob/main/data/output/sorted_portfolio_vw/unifactor_returns.csv)
    - [univariate-sorted portfolios](https://github.com/mlfina/China-A-Sort/blob/main/data/output/sorted_portfolio_vw/unisort_returns.csv)
    - [bivariate-sorted portfolios](https://github.com/mlfina/China-A-Sort/blob/main/data/output/sorted_portfolio_vw/bisort_returns.csv)

2. Equal-Weighted Sorted Portfolios

    - [univariate-sorted long-short factor](https://github.com/mlfina/China-A-Sort/blob/main/data/output/sorted_portfolio_ew/unifactor_returns.csv)
    - [univariate-sorted portfolios](https://github.com/mlfina/China-A-Sort/blob/main/data/output/sorted_portfolio_ew/unisort_returns.csv)
    - [bivariate-sorted portfolios](https://github.com/mlfina/China-A-Sort/blob/main/data/output/sorted_portfolio_ew/bisort_returns.csv)

## Logics

1. Calculate the China A-Share characteristics and returns

    - see: https://github.com/Quantactix/ChinaAShareEquityCharacteristics

2. Use this repo to calculate **sorted portfolios returns** and **long-short factors**

    - see: https://github.com/xinhe97/SortCS

3. Results are in folders, where include bivariate sorted returns, univariate sorted returns, and univariate sorted factors.

    - data/output/sorted_portfolio_vw
    - data/output/sorted_portfolio_ew

## Execution

    $ cd code
    $ sh run.sh

*notes*:

    - Assume linux user.
    - Go to the folder `code` and then run the commanda `sh run.sh`
    
## Caveate

This repo provides code for your reference, which is only for academic purposes and is not for commercial use. This repo does not disclose any confidential data or proprietary data. Specifically, this repo does not share the source data or intermediary data. Researcher can use open-source web crawler, or commercial data vendor, e.g. CSMAR, Wind, WRDS, for the input data.

# Contact

The contributer is open to any academic discussion and collaboration.

Xin He

xinhe9701@gmail.com

https://www.xinhesean.com
