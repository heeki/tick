# Tick Analytics
The goal of this sample project is to demonstrate a number of different Kinesis use cases:
* Kinesis producer -> Kinesis Data Stream -> Kinesis Analytics -> Kinesis Data Stream -> Kinesis consumer
* Kinesis producer -> Kinesis Data Stream -> Lambda EFO consumer

## Data Model: Tick
Sample data was retrieved from https://www.tickdata.com/product/nbbo/. That data should be placed under analytics/data.

For example, my directory structure looks as follows:
```
tick/data/SampleEquityData_US/CompanyInfo
tick/data/SampleEquityData_US/NBBO
tick/data/SampleEquityData_US/OMED
tick/data/SampleEquityData_US/Quote Bars
tick/data/SampleEquityData_US/Quotes
tick/data/SampleEquityData_US/Trades
```

With the trade data in place, the tick/test/analytics_env.sh needs to be updated with pointers to the data files as follows:
 ```bash
ANALYTICS_BASEPATH=/tick
ANALYTICS_PYTHONPATH=$ANALYTICS_BASEPATH/src

ANALYTICS_REF=$ANALYTICS_BASEPATH/tick/data/SampleEquityData_US/CompanyInfo/CompanyInfo.asc
ANALYTICS_DATA1=$ANALYTICS_BASEPATH/tick/data/SampleEquityData_US/Trades/14081.csv
ANALYTICS_DATA2=$ANALYTICS_BASEPATH/tick/data/SampleEquityData_US/Trades/23444.csv
ANALYTICS_DATA3=$ANALYTICS_BASEPATH/tick/data/SampleEquityData_US/Trades/23870.csv
ANALYTICS_DATA4=$ANALYTICS_BASEPATH/tick/data/SampleEquityData_US/Trades/27667.csv
ANALYTICS_DATA5=$ANALYTICS_BASEPATH/tick/data/SampleEquityData_US/Trades/28082.csv
```

## Infrastructure deployment
To build the Kinesis stream, execute the deploy script with the proper parameters.

```bash
iac/deploy.sh -p [profile] -t [template_file] -s [stack_name] -v [create|update]
iac/describe.sh -p [profile] -s [stack_name]
```

## Kinesis Data Streams
To properly run the environment, you'll want to run a consumer in separate terminal windows. The purposes here is
to force a consume into separate processes to emulate multiple consumers reading from the stream. Once each of the 
consumers is running and listening on its assigned shard, the producer can be run against all of the data. In this
case, the producer script is serially running through each data file, which is not ideal. For now, I'm executing
the producer shell script against a single input file, which is ultimately going to shard #2. Ultimately, the
producer shell script should probably run against each data file, backgrounding and allowing the system to run them
all in parallel. I'm a little concerned about latency of process context switching so I'm sticking with just
one for now.
```bash
python tick/src/consumer.py shardId-000000000000
python tick/src/consumer.py shardId-000000000001
python tick/src/consumer.py shardId-000000000002

tick/test/analytics_producer.sh
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
