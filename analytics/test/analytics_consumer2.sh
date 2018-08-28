#!/bin/bash

source analytics/test/analytics_env.sh
echo "BASEPATH=$ANALYTICS_BASEPATH"
echo "PYTHONPATH=$ANALYTICS_PYTHONPATH"

cd $ANALYTICS_BASEPATH
python analytics/src/consumer.py $KINESIS_TICK shardId-000000000001
