"""
Interaction encoder for generating settlement contract calls.

Encodes calldata for different AMM protocols to be executed
by the settlement contract.

  Based on the Rust baseline solver implementation.
"""

from typing import Optional, List, Tuple
import logging

try:
    from web3 import Web3
    from eth_abi import encode
except ImportError:
    # Fallback for environments without web3
    Web3 = None
    encode = None

from src.domain.solution import Interaction


class InteractionEncoder:
    """
    Encodes interactions for different AMM protocols.
    
    Generates the calldata needed for the settlement contract
    to execute swaps on various DEXs.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.w3 = Web3() if Web3 else None
    
    def encode_uniswap_v2_swap(
        self,
        pool_address: str,
        token_in: str,
        token_out: str,
        amount_in: int,
        amount_out_min: int,
        recipient: str = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"  # Settlement contract
    ) -> Interaction:
        """
        Encode a Uniswap V2 swap interaction.
        
        Args:
            pool_address: Address of the Uniswap V2 pair
            token_in: Input token address
            token_out: Output token address
            amount_in: Input amount in wei
            amount_out_min: Minimum output amount in wei
            recipient: Recipient of the output tokens
            
        Returns:
            Interaction object with encoded calldata
        """
        if not self.w3:
            # Fallback implementation without web3
            return self._encode_uniswap_v2_fallback(
                pool_address, token_in, token_out, amount_in, amount_out_min, recipient
            )
        
        # Determine which token is token0 and token1
        # In real implementation, would need to query the pair contract
        # For now, assume tokens are ordered
        token0 = min(token_in, token_out).lower()
        token1 = max(token_in, token_out).lower()
        
        # Determine amounts based on which token we're swapping
        if token_in.lower() == token0:
            amount0_out = 0
            amount1_out = amount_out_min
        else:
            amount0_out = amount_out_min
            amount1_out = 0
        
        # Encode swap function
        # function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data)
        function_selector = self.w3.keccak(
            text="swap(uint256,uint256,address,bytes)"
        )[:4]
        
        encoded_params = encode(
            ['uint256', 'uint256', 'address', 'bytes'],
            [amount0_out, amount1_out, recipient, b'']
        )
        
        calldata = function_selector + encoded_params
        
        return Interaction(
            target=pool_address,
            value="0",
            call_data=calldata.hex()
        )
    
    def _encode_uniswap_v2_fallback(
        self,
        pool_address: str,
        token_in: str,
        token_out: str,
        amount_in: int,
        amount_out_min: int,
        recipient: str
    ) -> Interaction:
        """Fallback implementation without web3 dependency."""
        # Simplified encoding - in production would need proper ABI encoding
        calldata = f"0x022c0d9f{amount_out_min:064x}{recipient[2:].lower()}{'00' * 64}"
        
        return Interaction(
            target=pool_address,
            value="0",
            call_data=calldata
        )
    
    def encode_balancer_swap(
        self,
        vault_address: str,
        pool_id: bytes,
        token_in: str,
        token_out: str,
        amount_in: int,
        amount_out_min: int,
        recipient: str = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
    ) -> Interaction:
        """
        Encode a Balancer V2 swap interaction.
        
        Args:
            vault_address: Balancer Vault address
            pool_id: Pool ID (32 bytes)
            token_in: Input token address
            token_out: Output token address
            amount_in: Input amount in wei
            amount_out_min: Minimum output amount in wei
            recipient: Recipient address
            
        Returns:
            Interaction object with encoded calldata
        """
        if not self.w3 or not encode:
            # Fallback implementation
            return self._encode_balancer_fallback(
                vault_address, pool_id, token_in, token_out, amount_in, amount_out_min, recipient
            )
        
        # Balancer uses a SingleSwap struct
        # struct SingleSwap {
        #     bytes32 poolId;
        #     SwapKind kind;  // 0 for GIVEN_IN
        #     address assetIn;
        #     address assetOut;
        #     uint256 amount;
        #     bytes userData;
        # }
        
        # Encode the swap function for Balancer V2 Vault
        function_selector = self.w3.keccak(
            text="swap((bytes32,uint8,address,address,uint256,bytes),"
                 "(address,bool,address,bool),uint256,uint256)"
        )[:4]
        
        # SingleSwap struct
        single_swap = (
            pool_id,
            0,  # SwapKind.GIVEN_IN
            Web3.to_checksum_address(token_in),
            Web3.to_checksum_address(token_out),
            amount_in,
            b''  # userData
        )
        
        # FundManagement struct
        fund_management = (
            recipient,  # sender
            False,  # fromInternalBalance
            recipient,  # recipient
            False   # toInternalBalance
        )
        
        encoded_params = encode(
            ['(bytes32,uint8,address,address,uint256,bytes)',
             '(address,bool,address,bool)',
             'uint256',
             'uint256'],
            [single_swap, fund_management, amount_out_min, 2**256 - 1]  # deadline
        )
        
        calldata = function_selector + encoded_params
        
        # Balancer swaps go through the Vault
        vault_address = vault_address or "0xBA12222222228d8Ba445958a75a0704d566BF2C8"  # Mainnet
        
        return Interaction(
            target=vault_address,
            value="0",
            call_data=calldata.hex()
        )
    
    def _encode_balancer_fallback(
        self,
        vault_address: str,
        pool_id: bytes,
        token_in: str,
        token_out: str,
        amount_in: int,
        amount_out_min: int,
        recipient: str
    ) -> Interaction:
        """Fallback implementation without web3 dependency."""
        # Simplified encoding - in production would need proper ABI encoding
        pool_id_hex = pool_id.hex() if isinstance(pool_id, bytes) else pool_id
        calldata = f"0x52bbbe29{pool_id_hex}{'00' * 24}{token_in[2:].lower()}{token_out[2:].lower()}{amount_in:064x}{'00' * 64}{recipient[2:].lower()}{'00' * 24}{amount_out_min:064x}{'ff' * 64}"
        
        return Interaction(
            target=vault_address,
            value="0",
            call_data=calldata
        )
    
    def encode_curve_swap(
        self,
        pool_address: str,
        token_in_index: int,
        token_out_index: int,
        amount_in: int,
        amount_out_min: int
    ) -> Interaction:
        """
        Encode a Curve swap interaction.
        
        Args:
            pool_address: Curve pool address
            token_in_index: Index of input token in pool
            token_out_index: Index of output token in pool
            amount_in: Input amount in wei
            amount_out_min: Minimum output amount in wei
            
        Returns:
            Interaction object with encoded calldata
        """
        if not self.w3:
            # Fallback implementation
            return self._encode_curve_fallback(
                pool_address, token_in_index, token_out_index, amount_in, amount_out_min
            )
        
        # Curve uses exchange function
        # function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy)
        function_selector = self.w3.keccak(
            text="exchange(int128,int128,uint256,uint256)"
        )[:4]
        
        encoded_params = encode(
            ['int128', 'int128', 'uint256', 'uint256'],
            [token_in_index, token_out_index, amount_in, amount_out_min]
        )
        
        calldata = function_selector + encoded_params
        
        return Interaction(
            target=pool_address,
            value="0",
            call_data=calldata.hex()
        )
    
    def _encode_curve_fallback(
        self,
        pool_address: str,
        token_in_index: int,
        token_out_index: int,
        amount_in: int,
        amount_out_min: int
    ) -> Interaction:
        """Fallback implementation without web3 dependency."""
        # Simplified encoding - in production would need proper ABI encoding
        calldata = f"0x3df021240000000000000000000000000000000000000000000000000000000000000000{token_in_index:02x}0000000000000000000000000000000000000000000000000000000000000000{token_out_index:02x}{amount_in:064x}{amount_out_min:064x}"

        return Interaction(target=pool_address, value="0", call_data=calldata)
