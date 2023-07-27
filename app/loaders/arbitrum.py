import requests
import json
import pandas as pd

from datetime import datetime, timedelta

from app.loaders.loader import Loader, LoaderType


class UniswapV3ArbitrumHourDataLoader(Loader):

    def __init__(self, pool: str, loader_type: LoaderType, decimals_diff: int) -> None:
        super().__init__(loader_type)
        self.pool = pool
        self.decimals_diff = decimals_diff
        self._url = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'

    def extract(self):
        query = """
        {
        liquidityPoolHourlySnapshots(
            first: 1000,
            orderBy:timestamp,
            where: {id_contains: "%s"},
            orderDirection: desc
        ) {
            timestamp
            tick
        }
        }
        """ % self.pool.lower()

        response = requests.post(self._url, json={'query': query})
        data = json.loads(response.text)
        
        if 'errors' in data:
            raise ValueError(f'Error in response: {data["errors"]}')

        self._data = pd.DataFrame(data['data']['liquidityPoolHourlySnapshots'])

    def transform(self):
        self._data['date'] = self._data['timestamp'].astype(int).apply(lambda x: datetime.utcfromtimestamp(x))
        # round to nearest upper hour
        self._data['date'] =\
            self._data['date'].apply(lambda x: x - timedelta(minutes=x.minute, seconds=x.second, microseconds=x.microsecond) + timedelta(hours=1))
        self.__preprocess_tick_to_price()

    def __preprocess_tick_to_price(self):
        self._data['tick'] = self._data['tick'].astype(int)
        self._data['price'] = self._data['tick'].apply(lambda x: (1.0001 ** x) * 10**(self.decimals_diff))

    def load(self):
        if self.loader_type == LoaderType.CSV:
            self._data.to_csv(f'./{self.pool}_uniswap_v3.csv', index=False)
        elif self.loader_type == LoaderType.JSON:
            self._data.to_json(f'./{self.pool}_uniswap_v3.json', orient='records')
        elif self.loader_type == LoaderType.SQL:
            raise NotImplementedError("SQL loader not implemented")
        else:
            raise ValueError(f'Loader type {self.loader_type} not supported')
    
    def read(self, with_run: bool = False) -> pd.DataFrame:

        if with_run:
            self.run()

        if self.loader_type == LoaderType.CSV:
            self._data = pd.read_csv(f'./{self.pool}_uniswap_v3.csv')
            self._data['date'] = pd.to_datetime(self._data['date'])
        elif self.loader_type == LoaderType.JSON:
            self._data = pd.read_json(f'./{self.pool}_uniswap_v3.json', orient='records')
            self._data['date'] = pd.to_datetime(self._data['date'])
        elif self.loader_type == LoaderType.SQL:
            raise NotImplementedError("SQL loader not implemented")
        else:
            raise ValueError(f'Loader type {self.loader_type} not supported')

        return self._data
