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
def task_9(data):
    data['resolver_addr'], data['resolver_abi'] = deploy_contract(
        'contracts_dns/resolvers/',
        'PublicResolver',[
        data['registry_addr'],
        data['name_wrapper_addr'],
        data['controller_addr'],
        data['reverse_addr']]
    )
    app_celery.send_task('workers.10_set_rule.task_10', 
                    kwargs= {'data': data})
    
    print('Task 9 is complete')

    