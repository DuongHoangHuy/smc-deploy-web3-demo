from celery import Celery
import os
from celery.signals import after_setup_logger
import logging
import sys

app_celery = Celery('workers', 
                    backend='rpc://',
                    broker= os.getenv('RABBIT_URL'))

app_celery.conf.task_routes = ([
    ('workers.1_deploy_ens.*', {'queue': 'queue_app_1'}),
    ('workers.2_setup_root.*', {'queue': 'queue_1_2'}),
    ('workers.3_deploy_reverse_registrar.*', {'queue': 'queue_2_3'}),
    ('workers.4_deploy_base.*', {'queue': 'queue_3_4'}),
    ('workers.5_deploy_metadata.*', {'queue': 'queue_4_5'}),
    ('workers.6_deploy_name_wrapper.*', {'queue': 'queue_5_6'}),
    ('workers.7_deploy_price.*', {'queue': 'queue_6_7'}),
    ('workers.8_deploy_controller.*', {'queue': 'queue_7_8'}),
    ('workers.9_deploy_public.*', {'queue': 'queue_8_9'}),
    ('workers.10_set_rule.*', {'queue': 'queue_9_10'})
],)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.addHandler(logging.StreamHandler(sys.stdout))