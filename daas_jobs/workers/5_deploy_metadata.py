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
def task_5(data):
    if(network == 'mainnet'):
        suffix = 'mainnet'
    else:
        suffix = 'goerli'
    
    uri = f'https://metadata.dotmeme.ai/{suffix}/'
    print(f'uri: {uri}')
    data['metadata_addr'], data['metadata_abi']  = deploy_contract('contracts_dns/wrapper/', 'StaticMetadataService', [uri])

    app_celery.send_task('workers.6_deploy_name_wrapper.task_6', 
                        kwargs= {'data': data})

    print('Task 5 is complete')