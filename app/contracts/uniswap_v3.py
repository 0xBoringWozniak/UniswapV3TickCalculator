from app.contracts.contract import Contract
from app.abis import UNISWAP_V3_POOL_ABI as ABI


class PoolContract(Contract):

    def __init__(self, address: str, node: str) -> None:
        super().__init__(address, ABI, node)

    def token0(self) -> str:
        return self._contract.functions.token0().call()
    
    def token1(self) -> str:
        return self._contract.functions.token1().call()

    def tick_spacing(self) -> int:
        return self._contract.functions.tickSpacing().call()
