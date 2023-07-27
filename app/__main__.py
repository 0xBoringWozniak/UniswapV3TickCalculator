import argparse

from app.pipeline import build_arb_pipeline, Pipeline, Config


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('pool_address', help="checksum pool address", type=str)
    parser.add_argument('time_range', help="time range in hours to calculate std", type=int)
    parser.add_argument('std_count', help="std count to calculate range", type=int)
    parser.add_argument('node', help="Node connection (https://arb1.arbitrum.io/rpc)", type=str)
    parser.add_argument('--read_data', action='store_true', help='Read data from storage instead loading from the graph')
    args = parser.parse_args()

    config = Config(TIME_RANGE=args.time_range, DP_COUNT=args.std_count)

    pipeline: Pipeline = build_arb_pipeline(config, args.pool_address, args.node)

    lower_tick, upper_tick = pipeline.start(with_run=not args.read_data)

    print(f'Lower tick, Upper tick: [{lower_tick}, {upper_tick}]')
