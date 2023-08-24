from flask import Flask, render_template, request
from celery import Celery, Task
# from  workers.celery_config import app_celery
import time

from celery import Celery

app_celery = Celery('workers', 
                    backend='rpc://',
                    broker='pyamqp://guest@localhost//')

app = Flask(__name__)

@app.get('/root')
def index():
    return render_template('index.html')

@app.post('/root')
def handle():
    number1 = int(request.form['number1'])
    number2 = int(request.form['number2'])
    print(number1, number2)

    res = app_celery.send_task('workers.1_deploy_ens.task_1', kwargs={'data': {}})
    app.logger.info(res.backend)

    # lấy name

    return 'hehe'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= '8000')
