import json
import sys
from utils.kinesis_std import Kinesis
from utils.kinesis_efo import KinesisEnhanced
from utils.util import Util


def main():
    log = Util.get_logger("consumer-enhanced")

    # TODO: convert to argparse
    kinesis_stream = sys.argv[1]
    kclient = Kinesis(kinesis_stream)
    shards = kclient.get_shards()
    for shard in shards:
        log.info("discovered {}".format(shard))

    shard_id = shards[0]
    consumer_name = sys.argv[2]
    with KinesisEnhanced(kinesis_stream, consumer_name) as eclient:
        consumers = eclient.get_stream_consumers()
        for consumer in consumers:
            log.info("type={}, values={}".format(type(consumer), consumer))
            eclient.subscribe(shard_id)


if __name__ == "__main__":
    main()
