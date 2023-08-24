from workers.celery_config import app_celery
from workers.worker_config import worker_config
from src.deploy import deploy_contract
import time
from utils.data_processing import read_data, write_data

DELAY = worker_config['DELAY']

# input: none
# output: address & abi of registry + root

@app_celery.task
def task_1(data):
    data['registry_addr'], data['registry_abi']  = deploy_contract('contracts_dns/registry/', 'ENSRegistry')
    data['root_addr'], data['root_abi'] = deploy_contract('contracts_dns/root/', 'Root', [data['registry_addr']])
    
    app_celery.send_task('workers.2_setup_root.task_2',
                         queue='queue_1_2',
                         kwargs= {'data': data})
    print('Task 1 is complete')
