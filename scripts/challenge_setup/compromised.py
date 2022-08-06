from scripts.helper.utils import *
from brownie import Exchange, DamnValuableNFT, TrustfulOracle, TrustfulOracleInitializer

# starting setup messages
message('setup_start')

# sources
sources = [
    '0xA73209FB1a42495120166736362A1DfA9F95A105',
    '0xe92401A4d3af5E446d93D11EEc806b1462b39D15',
    '0x81A5D6E50C214044bE44cA0CB057fe119097850c'
]

# tokens in pool and token initial supply
exchange_initial_eth_balance = ether_to_wei(9990)
initial_nft_price = ether_to_wei(999)

# import accounts
deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

# set balance of sources accounts
for address in sources:
    set_account_balance_hardhat(address, hex(ether_to_wei(2)))
    # check sources balances
    assert web3.eth.get_balance(address) == ether_to_wei(2)

# make the attacker balance 0.1 ETH
set_account_balance_hardhat(attacker.address, hex(ether_to_wei(0.1)))
# check attacker balance
assert attacker.balance() == ether_to_wei(0.1)

# deploy the contracts
trustful_oracle_initializer = TrustfulOracleInitializer.deploy(sources, ["DVNFT", "DVNFT", "DVNFT"], [initial_nft_price, initial_nft_price, initial_nft_price], _fromDeployer)
oracle = TrustfulOracle.at(trustful_oracle_initializer.oracle())
exchange = Exchange.deploy(oracle.address, _fromDeployer | value_dict(exchange_initial_eth_balance))
nft_token = DamnValuableNFT.at(exchange.token())

# check if solved
def solution_assertion():
    message('final_assertion_check')
    try: ############ SUCCESS CONDITIONS ############
        assert exchange.balance() == 0
        assert attacker.balance() > exchange_initial_eth_balance
        assert nft_token.balanceOf(attacker.address) == 0
        assert oracle.getMedianPrice("DVNFT") == initial_nft_price
        return True
    except:
        return False

# done setting up
message('setup_end')
