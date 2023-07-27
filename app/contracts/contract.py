from typing import List

from web3 import Web3


class Contract:

    def __init__(self, address: str, ABI: str, node: str, *args, **kwargs) -> None:
        self._node: Web3 = Web3(Web3.HTTPProvider(node))

        address: str = self._node.to_checksum_address(address)
        self._contract = self._node.eth.contract(address=address, abi=ABI)

    def get_functions(self) -> List[str]:
        return self._contract.all_functions()
    
    @property
    def address(self):
        return self._contract.address
    
    @property
    def abi(self):
        return self._contract.abi
