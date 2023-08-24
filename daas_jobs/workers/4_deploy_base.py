from workers.celery_config import app_celery
from src.deploy import web3, deploy_contract, send_transaction
from utils.data_processing import read_data, write_data
import time
from utils.namehash import namehash, keccak
from workers.worker_config import worker_config

DELAY = worker_config['DELAY']
# iutput: address & abi of registry + root
# output: address & abi of registry + root

# @app_celery.task
def task_4(data):  
    # registry_contract = web3.eth.contract(address=data['registry_addr'], abi=registry_abi)
    root_contract = web3.eth.contract(address=data['root_addr'], abi=data['root_abi'])


    # Step 2: BaseRegistrarImplementation
    data['registrar_addr'], data['registrar_abi'] = deploy_contract('contracts_dns/ethregistrar/', 
                                                    'BaseRegistrarImplementation', 
                                                    [data['registry_addr'], '0x' + namehash('meme').hex()])

    time.sleep(DELAY)

    func1 = root_contract.functions.setSubnodeOwner('0x' + keccak('addr'.encode('utf-8')).hex(), data['registrar_addr'])
    send_transaction(func1, 'Set controller of .meme for controller')

    app_celery.send_task('workers.5_deploy_metadata.task_5', 
                         kwargs= {'data': data})
    print('Task 4 is complete')
