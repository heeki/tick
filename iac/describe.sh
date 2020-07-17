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
KINESIS_ID=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickPhysicalId") | .OutputValue')
KINESIS_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickArn") | .OutputValue')
for var in {KINESIS_ID,KINESIS_ARN}; do echo "$var=${!var}"; done
fi

if [ "$STACK" == "tick-lambda" ]
then
OUTPUT=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK)
LAMBDA_ROLE_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutConsumerExecRoleArn") | .OutputValue')
LAMBDA_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutConsumerLambdaArn") | .OutputValue')
DLQ_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutConsumerDLQArn") | .OutputValue')
EVENT_MAPPING_ID=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutConsumerEventSourceMapping") | .OutputValue')

for var in {LAMBDA_ROLE_ARN,LAMBDA_ARN,DLQ_ARN,EVENT_MAPPING_ID}; do echo "$var=${!var}"; done
fi