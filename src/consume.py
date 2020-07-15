import argparse
from clients.consumer import Consumer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stream', required=True, help='tick-ingest')
    ap.add_argument('--shard', required=True, help='shardId-000000000000')
    ap.add_argument('--batch_size', required=False, help='500')
    ap.add_argument('--position', required=False, help='TRIM_HORIZON|LATEST')
    args = ap.parse_args()

    batch_size = int(args.batch_size) if args.batch_size is not None else 100
    position = args.position if args.position is not None else 'LATEST'
    c = Consumer(args.stream, args.shard, batch_size)
    c.consume(position)


if __name__ == "__main__":
    main()
