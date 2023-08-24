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
def task_6(data):
    # metadata = web3.eth.contract(address=metadata_addr, abi=metadata_abi)
    # registry = web3.eth.contract(address=registry_addr, abi=registry_abi)
    # registrar = web3.eth.contract(address=registrar_addr, abi=registrar_abi)

    data['name_wrapper_addr'], data['name_wrapper_abi'] = deploy_contract('contracts_dns/wrapper/',
                                                                          'NameWrapper',
                                                                          [data['registry_addr'], data['registrar_addr'], data['metadata_addr'], data['name']])
    
    app_celery.send_task('workers.7_deploy_price.task_7', 
                    kwargs= {'data': data})

    print('Task 6 is complete')
