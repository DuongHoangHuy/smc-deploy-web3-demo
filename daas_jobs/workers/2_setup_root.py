from workers.celery_config import app_celery
from src.deploy import web3, send_transaction, account_from
from utils.data_processing import read_data, write_data
import time
from workers.worker_config import worker_config

DELAY = worker_config['DELAY']
# iutput: address & abi of registry + root
# output: address & abi of registry + root

@app_celery.task
def task_2(data):
    ZERO_HASH = '0x0000000000000000000000000000000000000000000000000000000000000000'
    registry_contract = web3.eth.contract(address=data['registry_addr'], abi=data['registry_abi'])
    root_contract = web3.eth.contract(address=data['root_addr'], abi=data['root_abi'])

    owner = account_from['address']

    func1 = registry_contract.functions.setOwner(ZERO_HASH, data['root_addr'])
    send_transaction(func1, 'Setting owner of root node to root contract')

    time.sleep(DELAY)

    func2 = root_contract.functions.setController(owner, True)
    send_transaction(func2, 'Setting controller of root to owner')

    time.sleep(DELAY)

    hash = web3.solidity_keccak(['bytes'], [b'reverse']).hex()
    func3 = root_contract.functions.setSubnodeOwner(hash, owner)
    send_transaction(func3, 'Setting owner of .reverse to owner on root')

    time.sleep(DELAY)

    func4 = root_contract.functions.setSubnodeOwner(hash, owner)
    send_transaction(func4, 'Setting owner of .reverse to owner on registry')

    app_celery.send_task('workers.3_deploy_reverse_registrar.task_3', 
                         queue='queue_2_3',
                         kwargs= {'data': data})

    print('Task 2 is complete')