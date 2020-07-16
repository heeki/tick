#!/bin/bash

# kinesis variables
ANALYTICS_PYTHONPATH=src
ANALYTICS_RDATA=data/SampleEquityData_US/CompanyInfo/CompanyInfo.asc
ANALYTICS_DATA0=data/SampleEquityData_US/Trades/14081.csv
ANALYTICS_DATA1=data/SampleEquityData_US/Trades/23444.csv
ANALYTICS_DATA2=data/SampleEquityData_US/Trades/23870.csv
ANALYTICS_DATA3=data/SampleEquityData_US/Trades/27667.csv
ANALYTICS_DATA4=data/SampleEquityData_US/Trades/28082.csv

KINESIS_TICK=tick-ingest
KINESIS_VWAP=tick-vwap
KINESIS_SHARD0=shardId-000000000000
KINESIS_SHARD1=shardId-000000000001
KINESIS_SHARD2=shardId-000000000002

# sam variables
export ENV1=local1
export ENV2=local2