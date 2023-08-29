# 1. Import solcx
import solcx
# solcx.compile_solc('0.8.21')
# 2. If you haven't already installed the Solidity compiler, uncomment the following line
solcx.install_solc('0.4.5')

# 3. Compile contract
def compile_contract(path_deploy, deploy_contract_name):
    print('Start compile')
    temp_file = solcx.compile_files(
        f'{path_deploy}{deploy_contract_name}.sol',
        output_values=['abi', 'bin'],
        # solc_version='0.8.19'
    )

    deploy_contract = f'{path_deploy}{deploy_contract_name}.sol:{deploy_contract_name}'

    # 4. Export contract data
    abi = temp_file[deploy_contract]['abi']
    bytecode = temp_file[deploy_contract]['bin']

    print('End compile')

    return (abi, bytecode)