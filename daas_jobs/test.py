from  workers.celery_config import app_celery

data = {}

data['name'] = 'ethh'
app_celery.send_task('workers.1_deploy_ens.task_1', 
                queue='queue_app_1',
                kwargs= {'data': data})