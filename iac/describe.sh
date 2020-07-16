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

if [ "$STACK" == "tick-kinesis" ]
then
OUTPUT=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK)
TICK_ID=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickPhysicalId") | .OutputValue')
TICK_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickArn") | .OutputValue')
for var in {TICK_ID,TICK_ARN}; do echo "$var=${!var}"; done
fi

if [ "$STACK" == "tick-lambda" ]
then
OUTPUT=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK)
LAMBDA_ARN=$(echo $OUTPUT | jq --raw-output -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutConsumerLambdaArn") | .OutputValue')
for var in {LAMBDA_ARN}; do echo "$var=${!var}"; done
fi