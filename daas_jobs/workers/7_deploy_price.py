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
def task_7(data):
    oracleAddress = '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'
    # if (network.name !== 'mainnet') {
    #   const dummyOracle = await deploySMC('DummyOracle', ['100000000'])
    #   oracleAddress = dummyOracle.address
    # }

    print("oracleAddress", oracleAddress)

    data['price_oracle_addr'], data['price_oracle_abi'] =  deploy_contract(
        'contracts_dns/ethregistrar/',
        'StablePriceOracle',
        [oracleAddress,
        [0, 0, 1585489599188, 475646879756, 158548959919]]
    )

    app_celery.send_task('workers.8_deploy_controller.task_8', 
                    kwargs= {'data': data})
    
    print('Task 7 is complete')