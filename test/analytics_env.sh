#!/bin/bash

ANALYTICS_BASEPATH=/Users/heeki/Documents/Isengard/code/tick
ANALYTICS_PYTHONPATH=$ANALYTICS_BASEPATH/analytics/src

ANALYTICS_REF=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/CompanyInfo/CompanyInfo.asc
ANALYTICS_DATA1=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/14081.csv
ANALYTICS_DATA2=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/23444.csv
ANALYTICS_DATA3=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/23870.csv
ANALYTICS_DATA4=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/27667.csv
ANALYTICS_DATA5=$ANALYTICS_BASEPATH/analytics/data/SampleEquityData_US/Trades/28082.csv

KINESIS_TICK=tick-ingest
KINESIS_VWAP=tick-vwap