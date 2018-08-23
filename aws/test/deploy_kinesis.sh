#!/bin/bash

source aws/test/deploy_env.sh
echo "PROFILE=$PROFILE"

TEMPLATE=aws/templates/kinesis.yaml
STACK=tick-kinesis
PARAMS=ParameterKey=ParamName,ParameterValue=tick
VERB=update-stack
aws --profile $PROFILE cloudformation $VERB \
--stack-name $STACK \
--template-body file://$TEMPLATE \
--parameters $PARAMS \
--capabilities CAPABILITY_IAM

aws --profile $PROFILE cloudformation wait stack-create-complete --stack-name $STACK

#aws --profile $PROFILE cloudformation describe-stack-resources --stack-name $STACK | jq -c '.["StackResources"][] | {type:.ResourceType, id:.PhysicalResourceId}'
KINESIS_ID=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutPhysicalId") | .OutputValue' | tr -d '"')
KINESIS_ARN=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK | jq -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutArn") | .OutputValue' | tr -d '"')
echo "KINESIS_ID=$KINESIS_ID"
echo "KINESIS_ARN=$KINESIS_ARN"
