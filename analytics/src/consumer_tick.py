import sys
from utils.kinesis import Kinesis
from utils.util import Util


def main():
    log = Util.get_logger("consumer")

    kinesis_stream = sys.argv[1]
    kclient = Kinesis(kinesis_stream)
    shards = kclient.get_shards()
    for shard in shards:
        log.info("discovered {}".format(shard))

    shard_id = sys.argv[2]
    batch_size = 200
    log.info("processing {}".format(shard_id))
    kclient.get_continuous(shard_id, batch_size)


if __name__ == "__main__":
    main()
