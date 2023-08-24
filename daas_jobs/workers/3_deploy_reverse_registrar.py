from workers.celery_config import app_celery
from src.deploy import web3, deploy_contract, send_transaction
from utils.data_processing import read_data, write_data
import time
from utils.namehash import namehash, keccak
from workers.worker_config import worker_config

DELAY = worker_config['DELAY']
# iutput: address & abi of registry + root
# output: address & abi of registry + root

@app_celery.task
def task_3(data):
    registry_contract = web3.eth.contract(address=data['registry_addr'], abi=data['registry_abi'])
    # root_contract = web3.eth.contract(address=root_addr, abi=root_abi)

    # owner = registry_contract.functions.owner(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00').call()

    data['reverse_addr'], data['reverse_abi'] = deploy_contract('contracts_dns/reverseRegistrar/', 'ReverseRegistrar', [data['registry_addr']])

    time.sleep(DELAY)

    func1 = registry_contract.functions.setSubnodeOwner(
        '0x' + namehash('reverse').hex(),
        '0x' + keccak('addr'.encode('utf-8')).hex(),
        data['reverse_addr']
    )
    send_transaction(func1, 'Setting owner of .addr.reverse to ReverseRegistrar on registry')

    app_celery.send_task('workers.4_deploy_base.task_4', 
                         queue='queue_3_4',
                         kwargs= {'data': data})

    print('Task 3 is complete')