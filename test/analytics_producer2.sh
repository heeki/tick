#!/bin/bash

source analytics/test/analytics_env.sh
echo "BASEPATH=$ANALYTICS_BASEPATH"
echo "PYTHONPATH=$ANALYTICS_PYTHONPATH"

cd $ANALYTICS_BASEPATH
python analytics/src/producer_tick.py $ANALYTICS_REF $ANALYTICS_DATA2
