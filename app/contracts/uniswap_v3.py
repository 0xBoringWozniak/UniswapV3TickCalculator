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
    
    def slot0(self) -> tuple:
        return self._contract.functions.slot0().call()
    
    def get_current_price(self, decimals_diff: int) -> int:
        sqrt_price_x96 = self._contract.functions.slot0().call()[0]
        return ((sqrt_price_x96) / 2**96) ** 2 * 10 ** decimals_diff
