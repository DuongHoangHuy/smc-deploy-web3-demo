# 1. Add imports
from src.compile import abi, bytecode
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# 2. Add the Web3 provider logic here:
provider_rpc = {
    'development': 'http://localhost:9944',
    'alphanet': 'https://rpc.api.moonbase.moonbeam.network',
    'moonbeam': 'https://ethereum-goerli.publicnode.com'
}
web3 = Web3(Web3.HTTPProvider(provider_rpc['alphanet']))  # Change to correct network

# 3. Create address variable
account_from = {
    'private_key': os.getenv('PRIVATE_KEY'),
    'address': os.getenv('ADDRESS_FROM'),
}
def deploy_contract(_domain, _desc, _expiry):
    print(f'Attempting to deploy from account: { account_from["address"]}')

    # 4. Create contract instance
    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    # 5. Build constructor tx
    construct_txn = Contract.constructor(_domain, _desc, _expiry).build_transaction(
        {
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )

    # 6. Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(construct_txn, account_from['private_key'])

    # 7. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f'Contract deployed at address: { tx_receipt.contractAddress }')
    return f'Contract deployed at address: { tx_receipt.contractAddress }'