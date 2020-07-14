#!/bin/bash

source deploy_env.sh
echo "PROFILE=$PROFILE"

TEMPLATE=templates/kinesis.yaml
STACK=tick-kinesis
PARAMS=ParameterKey=ParamName,ParameterValue=tick
VERB=update
aws --profile $PROFILE cloudformation ${VERB}-stack \
--stack-name $STACK \
--template-body file://$TEMPLATE \
--parameters $PARAMS \
--capabilities CAPABILITY_IAM

aws --profile $PROFILE cloudformation wait stack-${VERB}-complete --stack-name $STACK

#aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | {type:.ResourceType, id:.PhysicalResourceId}'
TICK_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickPhysicalId") | .OutputValue' | tr -d '"') && echo "TICK_ID=$TICK_ID"
TICK_ARN=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutTickArn") | .OutputValue' | tr -d '"') && echo "TICK_ARN=$TICK_ARN"

VWAP_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutVwapPhysicalId") | .OutputValue' | tr -d '"') && echo "VWAP_ID=$VWAP_ID"
VWAP_ARN=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutVwapArn") | .OutputValue' | tr -d '"') && echo "VWAP_ARN=$VWAP_ARN"

#ANALYTICS_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutAnalytics") | .OutputValue' | tr -d '"') && echo "ANALYTICS_ID=$ANALYTICS_ID"
