# Tick Analytics
The goal of this sample project is to ingest sample tick data, pump the data into Kinesis Data Streams,
and calculate the VWAP (volume weighted average price) using Kinesis Analytics.

## Trade
Sample data was retrieved from https://www.tickdata.com/product/nbbo/. That data should be placed under analytics/data.

For example, my directory structure looks as follows:
```
analytics/data/SampleEquityData/US
    /CompanyInfo
    /NBBO
    /OMED
    /Quote Bars
    /Quotes
    /Trades
```

With the trade data in place, the analytics/test/analytics_env.sh needs to be updated with pointers to the data files as follows:
 ```
ANALYTICS_BASEPATH=/Users/heeki/Documents/Isengard/code/tick
ANALYTICS_PYTHONPATH=$ANALYTICS_BASEPATH/analytics/src

ANALYTICS_REF=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/CompanyInfo/CompanyInfo.asc
ANALYTICS_DATA1=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/14081.csv
ANALYTICS_DATA2=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/23444.csv
ANALYTICS_DATA3=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/23870.csv
ANALYTICS_DATA4=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/27667.csv
ANALYTICS_DATA5=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/28082.csv
```

## Infrastructure deployment
To build the Kinesis stream, first the aws/test/deploy_env.sh file needs to be updated with the aws cli profile.

```
aws/test/deploy_kinesis.sh
```