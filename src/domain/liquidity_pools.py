from typing import Optional
from dataclasses import dataclass
from src.domain.eth import Address, U256
from src.utils.amm_math import UniswapV2

@dataclass
class ConstantProductPool:
    """
    Baseado em shared::sources::uniswap_v2::pool_fetching::Pool do Rust.
    
    Esta classe é para PROCESSAMENTO interno, não para parsing de JSON!
    """
    address: Address
    tokens: tuple[Address, Address]  # Rust usa (H160, H160)
    reserves: tuple[U256, U256]      # Rust usa (U256, U256)
    fee: int  # Em basis points
    
    def get_amount_out(self, token_out: Address, input: tuple[U256, Address]) -> Optional[U256]:
        """
        Baseado em BaselineSolvable::get_amount_out do Rust.
        """
        amount_in, token_in = input
        
        # Encontrar índices dos tokens
        if self.tokens[0] == token_in and self.tokens[1] == token_out:
            reserve_in = self.reserves[0]
            reserve_out = self.reserves[1]
        elif self.tokens[1] == token_in and self.tokens[0] == token_out:
            reserve_in = self.reserves[1]
            reserve_out = self.reserves[0]
        else:
            return None  # Tokens não encontrados na pool
        
        # Calcular output
        output = UniswapV2.get_amount_out(
            amount_in.value,
            reserve_in.value,
            reserve_out.value,
            self.fee
        )
        
        return U256(output) if output > 0 else None
    
    def gas_cost(self) -> int:
        """
        Baseado em gas_cost() do Rust.
        Uniswap V2 geralmente usa ~110k gas
        """
        return 110000