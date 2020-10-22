include etc/execute_env.sh

kinesis:
	aws --profile ${PROFILE} cloudformation create-stack --stack-name ${KINESIS_STACK} --template-body file://${KINESIS_TEMPLATE} --parameters ${KINESIS_PARAMS} --capabilities CAPABILITY_IAM | jq

kinesis.update:
	aws --profile ${PROFILE} cloudformation update-stack --stack-name ${KINESIS_STACK} --template-body file://${KINESIS_TEMPLATE} --parameters ${KINESIS_PARAMS} --capabilities CAPABILITY_IAM | jq

kinesis.describe.efo:
	aws kinesis describe-stream-consumer --stream-arn ${KINESIS_ARN} --consumer-name tick-consumer | jq

consumer: consumer.package consumer.deploy

consumer.build:
	sam build --profile ${PROFILE} --template ${CONSUMER_TEMPLATE} --parameter-overrides ${CONSUMER_PARAMS} --build-dir build --manifest requirements.txt --use-container

consumer.package:
	sam package -t ${CONSUMER_TEMPLATE} --output-template-file ${CONSUMER_OUTPUT} --s3-bucket ${S3BUCKET}

consumer.deploy:
	sam deploy -t ${CONSUMER_OUTPUT} --stack-name ${CONSUMER_STACK} --parameter-overrides ${CONSUMER_PARAMS} --capabilities CAPABILITY_NAMED_IAM

consumer.local.invoke:
	sam local invoke -t ${CONSUMER_TEMPLATE} --parameter-overrides ${CONSUMER_PARAMS} --env-vars etc/envvars.json -e etc/event.json Fn

consumer.local.api:
	sam local start-api -t ${CONSUMER_TEMPLATE} --parameter-overrides ${CONSUMER_PARAMS}

consumer.consume0.std:
	python src/consume.py --type STD --stream ${KINESIS_INGEST} --shard ${KINESIS_SHARD0} --batch_size 100

consumer.consume0.efo:
	python src/consume.py --type EFO --stream ${KINESIS_INGEST} --shard ${KINESIS_SHARD0} --consumer tick-consumer

lambda.invoke:
	aws --profile ${PROFILE} lambda invoke --function-name ${CONSUMER_FN} --invocation-type RequestResponse --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "." > tmp/response.json
	cat tmp/response.json | jq -r ".LogResult" | base64 --decode

producer.produce1:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA1} --stream ${KINESIS_INGEST} --batch_size 100 --limit 1000

producer.produce2:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA2} --stream ${KINESIS_INGEST} --batch_size 100 --limit 1000

producer.produce3:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA3} --stream ${KINESIS_INGEST} --batch_size 100 --limit 1000

producer.produce4:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA4} --stream ${KINESIS_INGEST} --batch_size 100 --limit 1000

producer.produce5:
	python src/produce.py --rfile ${ANALYTICS_RDATA} --dfile ${ANALYTICS_DATA5} --stream ${KINESIS_INGEST} --batch_size 100 --limit 1000

test:
	$(eval P_SWAGGER_KEY=$(shell shasum -a 256 iac/swagger.yaml | awk '{print $$1}'))

clean:
	rm -rf build/*