from scripts.helper.utils import *
from brownie import NaiveReceiverLenderPool, FlashLoanReceiver

# starting setup messages
message('setup_start')

# tokens in pool and tokens in receiver
ETHER_IN_POOL = ether_to_wei(1000)
ETHER_IN_RECEIVER = ether_to_wei(10)

# import accounts
deployer, _fromDeployer, attacker, _fromAttacker, some_user, _fromSomeUser = define_from_acc(qty=3)

# deploy the contracts
pool = NaiveReceiverLenderPool.deploy(_fromDeployer)

# fund the pool
deployer.transfer(pool.address, ETHER_IN_POOL)

# confirm the balances are correct
assert pool.balance() == ETHER_IN_POOL
assert pool.fixedFee() == int(Decimal(repr(1e18)))

# deploy flash loan receiver
receiver = FlashLoanReceiver.deploy(pool.address, _fromDeployer)

# fund the receiver
deployer.transfer(receiver.address, ETHER_IN_RECEIVER)

# confirm the balances are correct
assert receiver.balance() == ETHER_IN_RECEIVER

# check if solved
def solution_assertion():
    message('final_assertion_check')
    try: ############ SUCCESS CONDITIONS ############
        # All ETH has been drained from the receiver
        assert receiver.balance() == 0
        assert pool.balance() == ETHER_IN_POOL + ETHER_IN_RECEIVER
        return True
    except:
        return False

# done setting up
message('setup_end')
