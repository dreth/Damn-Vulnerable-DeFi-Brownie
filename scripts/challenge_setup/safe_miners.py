from scripts.helper.utils import *
from brownie import DamnValuableToken, TrusterLenderPool

# starting setup messages
message('setup_start')

# deposit token amount and address
DEPOSIT_TOKEN_AMOUNT = ether_to_wei(2000042)
DEPOSIT_ADDRESS = '0x79658d35aB5c38B6b988C23D02e0410A380B8D5c'

# accounts
deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

# Deploy Damn Valuable Token contract
token = DamnValuableToken.deploy(_fromDeployer)

# Deposit the DVT tokens to the address
token.transfer(DEPOSIT_ADDRESS, DEPOSIT_TOKEN_AMOUNT, _fromDeployer)

# Ensure initial balances are correctly set
assert token.balanceOf(DEPOSIT_ADDRESS) == DEPOSIT_TOKEN_AMOUNT
assert token.balanceOf(attacker.address) == 0

# check if solved
def solution_assertion():
    message('final_assertion_check')
    try: ############ SUCCESS CONDITIONS ############
        # The attacker took all tokens available in the deposit address
        assert token.balanceOf(DEPOSIT_ADDRESS) == 0
        assert token.balanceOf(attacker.address) == DEPOSIT_TOKEN_AMOUNT
        return True
    except:
        return False

# done setting up
message('setup_end')
