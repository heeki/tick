#!/bin/bash

while getopts p:s: flag
do
    case "${flag}" in
        p) PROFILE=${OPTARG};;
        s) STACK=${OPTARG};;
    esac
done

function usage {
    echo "describe.sh -p [profile] -s [stack]" && exit 1
}

if [ -z "$PROFILE" ]; then usage; fi
if [ -z "$STACK" ]; then usage; fi

TICK_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickPhysicalId") | .OutputValue')
TICK_ARN=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickArn") | .OutputValue')
# VWAP_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutVwapPhysicalId") | .OutputValue' | tr -d '"') && echo "VWAP_ID=$VWAP_ID"
# VWAP_ARN=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutVwapArn") | .OutputValue' | tr -d '"') && echo "VWAP_ARN=$VWAP_ARN"
# ANALYTICS_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutAnalytics") | .OutputValue' | tr -d '"') && echo "ANALYTICS_ID=$ANALYTICS_ID"

for var in {TICK_ID,TICK_ARN}; do echo "$var=${!var}"; done
