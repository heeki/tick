include etc/environment.sh

kinesis:
	aws --profile ${PROFILE} cloudformation create-stack --stack-name ${KINESIS_STACK} --template-body file://${KINESIS_TEMPLATE} --parameters file://${KINESIS_PARAMS} --capabilities CAPABILITY_IAM | jq
kinesis.update:
	aws --profile ${PROFILE} cloudformation update-stack --stack-name ${KINESIS_STACK} --template-body file://${KINESIS_TEMPLATE} --parameters file://${KINESIS_PARAMS} --capabilities CAPABILITY_IAM | jq
kinesis.describe.efo:
	aws kinesis describe-stream-consumer --stream-arn ${O_KINESIS_ARN} --consumer-name tick-consumer | jq

cognito:
	aws --profile ${PROFILE} cloudformation create-stack --stack-name ${COGNITO_STACK} --template-body file://${COGNITO_TEMPLATE} --parameters file://${COGNITO_PARAMS} --capabilities CAPABILITY_IAM | jq
cognito.update:
	aws --profile ${PROFILE} cloudformation update-stack --stack-name ${COGNITO_STACK} --template-body file://${COGNITO_TEMPLATE} --parameters file://${COGNITO_PARAMS} --capabilities CAPABILITY_IAM | jq

lambda: lambda.package lambda.deploy
lambda.build:
	sam build --profile ${PROFILE} --template ${LAMBDA_TEMPLATE} --parameter-overrides ${LAMBDA_PARAMS} --build-dir build --manifest requirements.txt --use-container
lambda.package:
	sam package -t ${LAMBDA_TEMPLATE} --output-template-file ${LAMBDA_OUTPUT} --s3-bucket ${S3BUCKET}
lambda.deploy:
	sam deploy -t ${LAMBDA_OUTPUT} --stack-name ${LAMBDA_STACK} --parameter-overrides ${LAMBDA_PARAMS} --capabilities CAPABILITY_NAMED_IAM

lambda.local:
	sam local invoke -t ${LAMBDA_TEMPLATE} --parameter-overrides ${LAMBDA_PARAMS} --env-vars etc/envvars.json -e etc/event.json Fn | jq
lambda.local.api:
	sam local start-api -t ${LAMBDA_TEMPLATE} --parameter-overrides ${LAMBDA_PARAMS}
lambda.invoke.sync:
	aws --profile ${PROFILE} lambda invoke --function-name ${O_FN} --invocation-type RequestResponse --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "." > tmp/response.json
	cat tmp/response.json | jq -r ".LogResult" | base64 --decode
	cat tmp/fn.json | jq
lambda.invoke.async:
	aws --profile ${PROFILE} lambda invoke --function-name ${O_FN} --invocation-type Event --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "."

consume.std:
	python src/consume.py --type STD --stream ${O_KINESIS_INGEST} --shard ${P_KINESIS_SHARD0} --batch_size 100
consume.efo:
	python src/consume.py --type EFO --stream ${O_KINESIS_INGEST} --shard ${P_KINESIS_SHARD0} --consumer tick-consumer
produce.1:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA1} --stream ${O_KINESIS_INGEST} --batch_size 100 --limit 10000
produce.2:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA2} --stream ${O_KINESIS_INGEST} --batch_size 100 --limit 10000
produce.3:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA3} --stream ${O_KINESIS_INGEST} --batch_size 100 --limit 10000
produce.4:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA4} --stream ${O_KINESIS_INGEST} --batch_size 100 --limit 10000
produce.5:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA5} --stream ${O_KINESIS_INGEST} --batch_size 100 --limit 10000
