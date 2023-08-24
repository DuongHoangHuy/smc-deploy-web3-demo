from workers.celery_config import app_celery
from src.deploy import web3, deploy_contract, send_transaction, network
from utils.data_processing import read_data, write_data
import time
from utils.namehash import namehash, keccak
from workers.worker_config import worker_config

DELAY = worker_config['DELAY']
# iutput: address & abi of registry + root
# output: address & abi of registry + root

# @app_celery.task
def task_10(data):
    # registry_contract = web3.eth.contract(address=data['registry_addr'], abi=registry_abi)
    registrar_contract = web3.eth.contract(address=data['registrar_addr'], abi=data['registrar_abi'])
    name_wrapper_contract = web3.eth.contract(address=data['name_wrapper_addr'], abi=data['name_wrapper_abi'])
    reverse_contract = web3.eth.contract(address=data['reverse_addr'], abi=data['reverse_abi'])
    # price_oracle_contract = web3.eth.contract(address=price_oracle_addr, abi=price_oracle_abi)
    # controller_contract = web3.eth.contract(address=data['controller_addr'], abi=controller_abi)
    # resolver_contract = web3.eth.contract(address=resolver_addr, abi=resolver_abi)

    func1 = reverse_contract.functions.setDefaultResolver(data['resolver_addr'])
    send_transaction(func1, 'Set setDefaultResolver for reverseRegistrar')

    func2 = name_wrapper_contract.functions.setController(data['controller_addr'], True)
    send_transaction(func2, 'Set controller of nameWrapper for controller')

    func3 = registrar_contract.functions.addController(data['name_wrapper_addr'])
    send_transaction(func3, 'Set controller of registrar for nameWrapper')

    func4 = reverse_contract.functions.setController(data['controller_addr'], True)
    send_transaction(func4, 'Set controller of reverseRegistrar for controller')

    print('Task 10 is complete')