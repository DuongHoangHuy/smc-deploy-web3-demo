from flask import Flask, render_template, request
from markupsafe import escape
from src.deploy import deploy_contract
from datetime import datetime

app = Flask(__name__)

@app.route('/')    
def say_hello():
    return 'hello world'

@app.get("/register-domain")
def show_form():
    return render_template("index.html")

@app.post("/register-domain")
def handle_register_domain():
    domain = request.form['domain']
    description = request.form['description']
    expiry_date = request.form['expiry_date']

    date_object = datetime.strptime(expiry_date, "%Y-%m-%d")
    unix_timestamp = int(date_object.timestamp())
    res = deploy_contract(domain, description, unix_timestamp)

    return res

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= '8000')
