# 1. Add imports
from web3 import Web3
import os
from dotenv import load_dotenv
from src.compile import compile_contract
from web3.gas_strategies.time_based import fast_gas_price_strategy

load_dotenv()

# 2. Add the Web3 provider logic here:
provider_rpc = {
    'development': 'http://localhost:9944',
    'alphanet': 'https://rpc.api.moonbase.moonbeam.network',
    # 'moonbeam': 'https://ethereum-goerli.publicnode.com',
    'sepolia': 'https://little-young-diamond.ethereum-sepolia.discover.quiknode.pro/cdfa4b559074f4ce4e0287d05bd6dc6cf87a16c6/'
    }

network = 'alphanet'
web3 = Web3(Web3.HTTPProvider(provider_rpc[network]))  # Change to correct network

# 3. Create address variable
account_from = {
    'private_key': os.getenv('PRIVATE_KEY'),
    'address': os.getenv('ADDRESS_FROM'),
}

def send_transaction(func, task):
    tx = func.build_transaction(
        {
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    tx_create = web3.eth.account.sign_transaction(tx, account_from['private_key'])
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'{task} on tx: {tx_receipt["transactionHash"]}')

def deploy_contract(path_deploy, deploy_contract_name, args = []): 
    abi, bytecode = compile_contract(path_deploy, deploy_contract_name)
    print(f'Attempting to deploy from account: { account_from["address"]}')
    # 4. Create contract instance
    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    # 5. Build constructor tx
    web3.eth.set_gas_price_strategy(fast_gas_price_strategy)

    construct_txn = Contract.constructor(*args).build_transaction(  # Corrected method name
        {
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
            # 'maxFeePerGas': web3.to_wei('2', 'gwei'),
            # 'maxPriorityFeePerGas': web3.to_wei('1', 'gwei')
            # 'gas': 2000000
        }
    )

    # 6. Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(construct_txn, account_from['private_key'])

    # 7. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f'Contract deployed at address: { tx_receipt.contractAddress }')
    return (tx_receipt.contractAddress, abi)