import math

from dataclasses import dataclass
from datetime import timedelta
from typing import Tuple

from app.loaders import LoaderType, UniswapV3ArbitrumHourDataLoader, Loader
from app.contracts import PoolContract, ERC20


@dataclass
class Config:
    TIME_RANGE: int # time range in hours
    DP_COUNT: int # number of STD to calculate range


class Pipeline:

    def __init__(self, config: Config) -> None:
        self._config: Config = config

    def add_loader(self, loader: Loader):
        self._loader: Loader = loader

    def add_pool(self, pool: PoolContract):
        self._pool: PoolContract = pool

    def start(self, with_run: bool = True) -> Tuple[int, int]:

        # read pool data
        self._data = self._loader.read(with_run=with_run)

        # filter data by date by timerange
        self._data = self._data[self._data['date'] >= self._data['date'].max() - timedelta(hours=self._config.TIME_RANGE)]

        # calculate std of price
        std = self._data['price'].pct_change().std()

        # get last price
        last_price = self._data['price'].iloc[-1]

        std_count = self._config.DP_COUNT
        range_lower, range_upper = (last_price - std_count * std * last_price, last_price + std_count * std * last_price)

        tick_spacing: int = self._pool.tick_spacing()
        scaler: int = 10 ** self._loader.decimals_diff
        return (self.get_initialized_tick_at_price(range_lower/scaler, tick_spacing), self.get_initialized_tick_at_price(range_upper/scaler, tick_spacing))

    @staticmethod
    def get_initialized_tick_at_price(price: float, tick_space: int) -> int:
        def price_to_tick(price):
            return int(math.floor(math.log(price) / math.log(1.0001)))

        raw = price_to_tick(price)
        if raw % tick_space < (tick_space // 2):
            return raw - raw % tick_space
        else:
            return raw + (60 - raw % tick_space)


def build_arb_pipeline(config: Config, pool_address: str, node: str, loader_type: LoaderType = LoaderType.CSV) -> Pipeline:

    pipeline: Pipeline = Pipeline(config)
    pool_contract = PoolContract(pool_address, node)
    pipeline.add_pool(pool_contract)

    token0 = ERC20(pool_contract.token0(), node)
    token1 = ERC20(pool_contract.token1(), node)
    decimals_diff = abs(token0.decimals() - token1.decimals())

    loader = UniswapV3ArbitrumHourDataLoader(pool_address, loader_type, decimals_diff)
    pipeline.add_loader(loader)

    return pipeline


if __name__ == "__main__":
    config = Config(TIME_RANGE=96, DP_COUNT=10)
    NODE = "https://arbitrum-mainnet.infura.io/v3/3c9943304cf64593a4013a87cc5fd3f5"
    POOL = "0xc6f780497a95e246eb9449f5e4770916dcd6396a"
    pipeline = build_arb_pipeline(config, POOL, NODE)
    print(pipeline.start())
