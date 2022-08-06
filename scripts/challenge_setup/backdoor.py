from scripts.helper.utils import *
from brownie import DamnValuableToken, WalletRegistry

# starting setup messages
message('setup_start')

# tokens in lender pool
AMOUNT_TOKENS_DISTRIBUTED = ether_to_wei(40)

# get signers
deployer, _fromDeployer = define_from_acc(qty=1)
(alice, _fromAlice, bob, _fromBob, charlie, _fromCharlie, david, _fromDavid) = define_from_acc(start=1,qty=4)
attacker, _fromAttacker = define_from_acc(start=5, qty=1)

# users
users = [x.address for x in [alice, bob, charlie, david]]
fromUsers = [_fromAlice, _fromBob, _fromCharlie, _fromDavid]

# load Gnosis contracts from ABI and bytecode
GnosisSafeABI, GnosisSafeBytecode = load_abi_and_bytecode_json('contracts/build-gnosis-safe/GnosisSafe.json')
GnosisSafeProxyFactoryABI, GnosisSafeProxyFactoryBytecode = load_abi_and_bytecode_json('contracts/build-gnosis-safe/GnosisSafeProxyFactory.json')

# Deploy Gnosis Safe master copy and factory contracts
master_copy = load_contract_from_abi_and_bytecode('GnosisSafe', GnosisSafeABI, GnosisSafeBytecode)
wallet_factory = load_contract_from_abi_and_bytecode(contract_name='GnosisSafeProxyFactory', abi=GnosisSafeProxyFactoryABI, bytecode=GnosisSafeProxyFactoryBytecode, constructor_params=[(master_copy.address, 'address')])
token = DamnValuableToken.deploy(_fromDeployer)

# Deploy the registry
wallet_registry = WalletRegistry.deploy( 
    master_copy.address,
    wallet_factory.address,
    token.address,
    users,
    _fromDeployer
)

# Users are registered as beneficiaries
for user in users:
    assert wallet_registry.beneficiaries(user) == True

# Transfer tokens to be distributed to the registry
token.transfer(wallet_registry.address, AMOUNT_TOKENS_DISTRIBUTED, _fromDeployer)

# check if solved
def solution_assertion():
    message('final_assertion_check')
    try: ############ SUCCESS CONDITIONS ############
        for user in users:
            wallet = wallet_registry.wallets(user)

            # User must have registered a wallet
            assert wallet != ZERO_ADDRESS

            # User is no longer registered as a beneficiary
            assert wallet_registry.beneficiaries(user) == False

        # Attacker must have taken all tokens
        assert token.balanceOf(attacker) == AMOUNT_TOKENS_DISTRIBUTED

        return True
    except:
        return False

# done setting up
message('setup_end')
