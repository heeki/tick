include etc/execute_env.sh

sam: sam.package sam.deploy

sam.build:
	sam build --profile ${PROFILE} --template ${CONSUMER_TEMPLATE} --parameter-overrides ${CONSUMER_PARAMS} --build-dir build --manifest requirements.txt --use-container

sam.package:
	sam package -t ${CONSUMER_TEMPLATE} --output-template-file ${CONSUMER_OUTPUT} --s3-bucket ${S3BUCKET}

sam.deploy:
	sam deploy -t ${CONSUMER_OUTPUT} --stack-name ${CONSUMER_STACK} --parameter-overrides ${CONSUMER_PARAMS} --capabilities CAPABILITY_NAMED_IAM

sam.local.invoke:
	sam local invoke -t ${CONSUMER_TEMPLATE} --parameter-overrides ${CONSUMER_PARAMS} --env-vars etc/envvars.json -e etc/event.json Fn

sam.local.api:
	sam local start-api -t ${CONSUMER_TEMPLATE} --parameter-overrides ${CONSUMER_PARAMS}

lambda.invoke:
	aws --profile ${PROFILE} lambda invoke --function-name ${CONSUMER_FN} --invocation-type RequestResponse --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "." > tmp/response.json
	cat tmp/response.json | jq -r ".LogResult" | base64 --decode

kinesis:
	aws --profile ${PROFILE} cloudformation create-stack --stack-name ${KINESIS_STACK} --template-body file://${KINESIS_TEMPLATE} --parameters ${KINESIS_PARAMS} --capabilities CAPABILITY_IAM | jq

kinesis.update:
	aws --profile ${PROFILE} cloudformation update-stack --stack-name ${KINESIS_STACK} --template-body file://${KINESIS_TEMPLATE} --parameters ${KINESIS_PARAMS} --capabilities CAPABILITY_IAM | jq

test:
	$(eval P_SWAGGER_KEY=$(shell shasum -a 256 iac/swagger.yaml | awk '{print $$1}'))

clean:
	rm -rf build/*