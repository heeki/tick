#!/bin/bash

source analytics/test/analytics_env.sh
echo "BASEPATH=$ANALYTICS_BASEPATH"
echo "PYTHONPATH=$ANALYTICS_PYTHONPATH"

cd $ANALYTICS_BASEPATH
python analytics/src/consumer_vwap.py $KINESIS_VWAP shardId-000000000000
