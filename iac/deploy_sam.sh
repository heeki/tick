#!/bin/bash

while getopts p:t:s:b: flag
do
    case "${flag}" in
        p) PROFILE=${OPTARG};;
        t) TEMPLATE=${OPTARG};;
        s) STACK=${OPTARG};;
        b) S3BUCKET=${OPTARG};;
    esac
done

function usage {
    echo "deploy_sam.sh -p [profile] -t [template_file] -s [stack_name] -b [bucket]" && exit 1
}

if [ -z "$PROFILE" ]; then usage; fi
if [ -z "$TEMPLATE" ]; then usage; fi
if [ -z "$STACK" ]; then usage; fi
if [ -z "$S3BUCKET" ]; then usage; fi

sam package \
--template-file iac/sam_input.yaml \
--output-template-file iac/sam_output.yaml \
--s3-bucket $S3BUCKET

echo "Deploying Lambda stack ($STACK)..."
PARAMS="ParamEnv1=$ENV1 ParamEnv2=$ENV2"
sam deploy \
--template-file iac/sam_output.yaml \
--stack-name $STACK \
--parameter-overrides $PARAMS \
--capabilities CAPABILITY_NAMED_IAM
