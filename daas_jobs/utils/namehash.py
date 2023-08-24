from src.deploy import web3
# hash = web3.solidity_keccak(['bytes'], [b'reverse']).hex()

def keccak(_name):
  return web3.to_bytes(hexstr = web3.solidity_keccak(['bytes'], [_name]).hex())

def namehash(name):
  if name == '':
    return web3.to_bytes(hexstr='0x' + '00' * 32)
  else:
    label, _, remainder = name.partition('.')
    return keccak(namehash(remainder) + keccak(label.encode('utf-8')))