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
def task_8(data):
    data['controller_addr'], data['controller_abi'] = deploy_contract(
        'contracts_dns/ethregistrar/',
        'ETHRegistrarController', [
        data['registrar_addr'],
        data['price_oracle_addr'],
        60,
        86400,
        data['reverse_addr'],
        data['name_wrapper_addr'],
        data['registry_addr']
      ]
    )

    app_celery.send_task('workers.9_deploy_public.task_9', 
                    kwargs= {'data': data})

    print('Task 8 is complete')
