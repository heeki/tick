import argparse
from clients.producer import Producer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rfile', required=True, help='data/SampleEquityData_US/CompanyInfo/CompanyInfo.asc')
    ap.add_argument('--dfile', required=True, help='data/SampleEquityData_US/Trades/14081.csv')
    ap.add_argument('--stream', required=True, help='tick-ingest')
    ap.add_argument('--batch_size', required=False, help='500')
    args = ap.parse_args()

    batch_size = int(args.batch_size) if args.batch_size is not None else 100
    p = Producer(args.rfile, args.dfile, args.stream, batch_size)
    p.produce()


if __name__ == "__main__":
    main()
