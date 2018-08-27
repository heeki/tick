#!/bin/bash

source analytics/test/analytics_env.sh
echo "BASEPATH=$ANALYTICS_BASEPATH"
echo "PYTHONPATH=$ANALYTICS_PYTHONPATH"

cd $ANALYTICS_BASEPATH
python analytics/src/consumer.py shardId-000000000000
python analytics/src/consumer.py shardId-000000000001
python analytics/src/consumer.py shardId-000000000002
