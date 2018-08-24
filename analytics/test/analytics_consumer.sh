#!/bin/bash

source analytics/test/analytics_env.sh
echo "BASEPATH=$ANALYTICS_BASEPATH"
echo "PYTHONPATH=$ANALYTICS_PYTHONPATH"

cd $ANALYTICS_BASEPATH
#python analytics/src/consumer.py $ANALYTICS_REF $ANALYTICS_DATA1
#python analytics/src/consumer.py $ANALYTICS_REF $ANALYTICS_DATA2
#python analytics/src/consumer.py $ANALYTICS_REF $ANALYTICS_DATA3
python analytics/src/consumer.py $ANALYTICS_REF $ANALYTICS_DATA4
#python analytics/src/consumer.py $ANALYTICS_REF $ANALYTICS_DATA5
