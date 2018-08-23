#!/bin/bash

source analytics/test/analytics_env.sh
BASEPATH=$ANALYTICS_BASEPATH
PYTHONPATH=$ANALYTICS_PYTHONPATH
echo "BASEPATH=$BASEPATH"
echo "PYTHONPATH=$PYTHONPATH"

cd $BASEPATH
python analytics/src/client.py