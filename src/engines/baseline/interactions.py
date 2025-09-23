"""Build settlement contract interactions."""

from web3 import Web3
from eth_abi import encode
from src.domain.solution import Interaction

class InteractionBuilder:
    """Builds interactions for settlement contract."""
    
    def build_amm_interaction(
        self,
        pool_address: str,
        token_in: str,
        token_out: str,
        amount_in: int
    ) -> Interaction:
        """Build AMM swap interaction."""
        # Encode swap function call
        selector = Web3.keccak(text="swap(uint256,uint256,address,bytes)")[:4]
        calldata = selector + encode(
            ['uint256', 'uint256', 'address', 'bytes'],
            [amount_in, 0, pool_address, b'']
        )
        
        return Interaction(
            target=pool_address,
            value=0,
            call_data=calldata.hex()
        )