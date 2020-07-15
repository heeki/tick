import argparse
import sys
from utils.kinesis_std import Kinesis
from utils.util import Util


log = Util.get_logger("consumer")


def init():
    global batch_size, company_id, mapper

    ap = argparse.ArgumentParser()
    ap.add_argument('--stream', required=True, help='tick-ingest')
    ap.add_argument('--shard', required=True, help='shardId-000000000000')
    ap.add_argument('--batch_size', required=False, help='500')
    args = ap.parse_args()

    batch_size = int(args.batch_size) if args.batch_size is not None else 100
    company_id = args.dfile.split('/')[-1].split('.')[0]
    with open(args.rfile, 'r') as csv_file:
        ref_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(ref_reader, None)
        for ref_data in ref_reader:
            ref = Symbol(ref_data)
            mapper[ref.company_id] = ref

    return args


def main():
    kinesis_stream = sys.argv[1]
    kclient = Kinesis(kinesis_stream)
    shards = kclient.get_shards()
    for shard in shards:
        log.info("discovered {}".format(shard))

    shard_id = sys.argv[2]
    batch_size = 1
    log.info("processing {}".format(shard_id))
    kclient.get_continuous(shard_id, batch_size)


if __name__ == "__main__":
    main()
