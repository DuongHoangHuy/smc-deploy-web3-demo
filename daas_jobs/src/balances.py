# 1. Add import
from web3 import Web3

# 1. Add the Web3 provider logic here:
provider_rpc = {
    'development': 'http://localhost:9944',
    'alphanet': 'https://rpc.api.moonbase.moonbeam.network',
}
web3 = Web3(Web3.HTTPProvider(provider_rpc['alphanet']))  # Change to correct network

# 2. Create address variables
address_from = '0x097447fc31B683306d41D7127FFDe7262D6a33f2'
address_to = '0xB39d5e1B07d5E40c0DC0ab1C5a39068F5787C3F9'

# 3. Fetch balance data
balance_from = web3.from_wei(web3.eth.get_balance(address_from), 'ether')
balance_to = web3.from_wei(web3.eth.get_balance(address_to), 'ether')

print(f'The balance of { address_from } is: { balance_from } ETH')
print(f'The balance of { address_to } is: { balance_to } ETH')
