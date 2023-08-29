import os
from flask import Flask, render_template, request
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app_celery = Celery('workers', 
                    backend='rpc://',
                    # broker='pyamqp://guest@localhost//'
                    broker= os.getenv('RABBIT_URL')
                    )

app = Flask(__name__)

@app.get('/root')
def index():
    return render_template('index.html')

@app.post('/root')
def handle(): 
    data = {'name': request.form['name']}
    res = app_celery.send_task('workers.1_deploy_ens.task_1', 
                               queue='queue_app_1',
                               kwargs={'data': data})
    return f'send data: {data}'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= '8000')
