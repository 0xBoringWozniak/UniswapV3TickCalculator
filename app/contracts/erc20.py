from app.contracts.contract import Contract
from app.abis.erc20 import ABI as ERC20_ABI

from app.contracts.uniswap_v3 import PoolContract


class ERC20(Contract):

    def __init__(self, address: str, node: str) -> None:
        super().__init__(address, ERC20_ABI, node)

    def decimals(self) -> int:
        return self._contract.functions.decimals().call()
