# Tick Analytics
The goal of this sample project is to demonstrate a number of different Kinesis use cases:
* Kinesis producer -> Kinesis Data Stream -> Kinesis Analytics -> Kinesis Data Stream -> Kinesis consumer
* Kinesis producer -> Kinesis Data Stream -> Lambda EFO consumer

## Data Model: Tick
Sample data was retrieved from https://www.tickdata.com/product/nbbo/. That data should be placed under analytics/data.

For example, my directory structure looks as follows:
```
data/SampleEquityData_US/CompanyInfo
data/SampleEquityData_US/NBBO
data/SampleEquityData_US/OMED
data/SampleEquityData_US/Quote Bars
data/SampleEquityData_US/Quotes
data/SampleEquityData_US/Trades
```

## Infrastructure Deployment
To build the Kinesis stream, execute the `makefile`: `make kinesis`.


## Kinesis Producer
To produce data into the stream:
```bash
source src/environment.sh
python src/produce.py --rfile $ANALYTICS_RDATA --dfile $ANALYTICS_DATA0 --stream $KINESIS_TICK --batch_size 100
python src/produce.py --rfile $ANALYTICS_RDATA --dfile $ANALYTICS_DATA1 --stream $KINESIS_TICK --batch_size 100
python src/produce.py --rfile $ANALYTICS_RDATA --dfile $ANALYTICS_DATA2 --stream $KINESIS_TICK --batch_size 100
python src/produce.py --rfile $ANALYTICS_RDATA --dfile $ANALYTICS_DATA3 --stream $KINESIS_TICK --batch_size 100
python src/produce.py --rfile $ANALYTICS_RDATA --dfile $ANALYTICS_DATA4 --stream $KINESIS_TICK --batch_size 100
```

## Kinesis Consumer
To consume data from the stream:
```bash
source src/environment.sh
python src/consume.py --type STD --stream $KINESIS_TICK --shard $KINESIS_SHARD0 --batch_size 100
python src/consume.py --type STD --stream $KINESIS_TICK --shard $KINESIS_SHARD1 --batch_size 100
python src/consume.py --type STD --stream $KINESIS_TICK --shard $KINESIS_SHARD2 --batch_size 100
python src/consume.py --type EFO --stream $KINESIS_TICK --shard $KINESIS_SHARD0 --consumer tick-consumer0
python src/consume.py --type EFO --stream $KINESIS_TICK --shard $KINESIS_SHARD1 --consumer tick-consumer1
python src/consume.py --type EFO --stream $KINESIS_TICK --shard $KINESIS_SHARD2 --consumer tick-consumer2
```

## Kinesis Analytics
To calculate VWAP on the live stream, we need to first create a destination stream ("VWAP_DESTINATION"). Then
we need to create a pump ("VWAP_PUMP"), which will read the source stream ("SOURCE_SQL_STREAM_001"), calculate
the VWAP, and place the results in the destination stream.

```sql
CREATE OR REPLACE STREAM "VWAP_DESTINATION" ("symbol" VARCHAR(4), "vwap" REAL, "earliest_epoch" DOUBLE);

CREATE OR REPLACE PUMP "VWAP_PUMP" AS INSERT INTO "VWAP_DESTINATION"
SELECT STREAM "symbol", SUM("volume" * "price") / SUM("volume") as vwap, MIN("ingest_epoch") as earliest_epoch
FROM "SOURCE_SQL_STREAM_001"
GROUP BY "symbol", STEP("SOURCE_SQL_STREAM_001".ROWTIME BY INTERVAL '1' SECOND);
```

## Lambda Tumbling Windows
Updated the repository to test out tumbling windows with Lambda, which allows for 1MB of state to carry over from invoke to invoke.