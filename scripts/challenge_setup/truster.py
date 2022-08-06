from scripts.helper.utils import *
from brownie import DamnValuableToken, TrusterLenderPool

# starting setup messages
message('setup_start')

# tokens in pool
TOKENS_IN_POOL = ether_to_wei(1000000)

# import accounts
deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

# deploy the contracts
token = DamnValuableToken.deploy(_fromDeployer)
pool = TrusterLenderPool.deploy(token.address, _fromDeployer)

# fund the pool
token.transfer(pool.address, TOKENS_IN_POOL, _fromDeployer)

# confirm the balances are correct
assert token.balanceOf(pool.address) == TOKENS_IN_POOL
assert token.balanceOf(attacker.address) == 0

# check if solved
def solution_assertion():
    message('final_assertion_check')
    try: ############ SUCCESS CONDITIONS ############
        # Attacker has taken all tokens from the pool
        assert token.balanceOf(attacker.address) == TOKENS_IN_POOL
        assert token.balanceOf(pool.address) == 0
        return True
    except:
        return False

# done setting up
message('setup_end')
