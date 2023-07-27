# UniswapPoolPrep

The script calculates the position's range for given params `DP_COUNT` (number of `STD`) and `TIME_RANGE` (period per each we need to calculate `STD`)

## How to run

### Install
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### How to use
```
usage: __main__.py [-h] [--read_data] pool_address time_range std_count node

positional arguments:
  pool_address  checksum pool address
  time_range    time range in hours to calculate std
  std_count     std count to calculate range
  node          Node connection (https://arb1.arbitrum.io/rpc)

optional arguments:
  -h, --help    show this help message and exit
  --read_data   Read data from storage instead loading from the graph
```

### Example

```
python3 -m app 0xC31E54c7a869B9FcBEcc14363CF510d1c41fa443 24 8 https://arbitrum-mainnet.infura.io/v3/mynode
Lower tick, Upper tick: [-201250, -200820]
```

## Notes
- Sometimes you can get an error `ValueError: Error in response: [{'message': 'Store error: database unavailable'}]` which means that Uniswap V3 subgraph is unavailable now. Try to run app later or with another IP.
- All available pools can be found [here](https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum/graphql?query=%0A++++%23%0A++++%23+Welcome+to+The+GraphiQL%0A++++%23%0A++++%23+GraphiQL+is+an+in-browser+tool+for+writing%2C+validating%2C+and%0A++++%23+testing+GraphQL+queries.%0A++++%23%0A++++%23+Type+queries+into+this+side+of+the+screen%2C+and+you+will+see+intelligent%0A++++%23+typeaheads+aware+of+the+current+GraphQL+type+schema+and+live+syntax+and%0A++++%23+validation+errors+highlighted+within+the+text.%0A++++%23%0A++++%23+GraphQL+queries+typically+start+with+a+%22%7B%22+character.+Lines+that+start%0A++++%23+with+a+%23+are+ignored.%0A++++%23%0A++++%23+An+example+GraphQL+query+might+look+like%3A%0A++++%23%0A++++%23+++++%7B%0A++++%23+++++++field%28arg%3A+%22value%22%29+%7B%0A++++%23+++++++++subField%0A++++%23+++++++%7D%0A++++%23+++++%7D%0A++++%23%0A++++%23+Keyboard+shortcuts%3A%0A++++%23%0A++++%23++Prettify+Query%3A++Shift-Ctrl-P+%28or+press+the+prettify+button+above%29%0A++++%23%0A++++%23+++++Merge+Query%3A++Shift-Ctrl-M+%28or+press+the+merge+button+above%29%0A++++%23%0A++++%23+++++++Run+Query%3A++Ctrl-Enter+%28or+press+the+play+button+above%29%0A++++%23%0A++++%23+++Auto+Complete%3A++Ctrl-Space+%28or+just+start+typing%29%0A++++%23%0A++).
- All data will be save in project root directory as a CSV, after that you can use `--read_data`
