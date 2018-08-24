from utils.kinesis import Kinesis
from utils.util import Util
from tick.symbol import Symbol
from tick.trade import Trade


def main():
    log = Util.get_logger("consumer")

    kinesis_stream = "tick-ingest"
    kclient = Kinesis(kinesis_stream)
    shards = kclient.get_shards()
    for shard in shards:
        log.info("discovered {}".format(shard))

    kclient.get_continuous("shardId-000000000002", log)


if __name__ == "__main__":
    main()
