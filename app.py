from flask import Flask, request, abort, g
import logging
import sqlite3
from flask_cors import CORS
import json
import requests as req
import os


from twilio_integration import send_message, send_recovery_message
from mailgun_integration import send_email, send_recovery_email
from generate_id import generate_id
from database import *


app = Flask(__name__)
CORS(app)


app.config.from_mapping(
    SECRET_KEY=os.environ.get("key-id-pro")
)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello():
    return 'This should not be visible!'

@app.route('/send', methods=['POST'])
def send_code():
    id = generate_id()

    params = {
        'email': request.form['email'],
        'sms': request.form['sms'],
        'phone': request.form['phone'],
        'emailAddress': request.form['emailAddress'],
        'captcha': request.form['captcha']
    }

    captcha_response = req.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret':  os.environ.get("recaptcha-id-pro"),
        'response': params['captcha']
    })

    if not json.loads(captcha_response.text)['success']:
        abort(403)

    if params['sms'] == "true" and params['email'] == "true":
        if verify_phone_not_present(params['phone']) and verify_email_not_present(params['emailAddress']):
            insert_id(id, params['emailAddress'], params['phone'])
            send_message(params['phone'], id)
            send_email(params['emailAddress'], id)
        else:
            if not verify_email_not_present(params['emailAddress']):
                send_recovery_email(params['emailAddress'], get_id_by_email(params['emailAddress']))
            if not verify_phone_not_present(params['phone']):
                send_recovery_message(params['phone'], get_id_by_phone(params['phone']))
    elif params['sms'] == "true":
        if verify_phone_not_present(params['phone']):
            insert_id(id, "-", params['phone'])
            send_message(params['phone'], id)
        else:
            send_recovery_message(params['phone'], get_id_by_phone(params['phone']))
    elif params['email'] == "true":
        if verify_email_not_present(params['emailAddress']):
            insert_id(id, params['emailAddress'], "-")
            send_email(params['emailAddress'], id)
        else:
            send_recovery_email(params['emailAddress'], get_id_by_email(params['emailAddress']))
    else:
        abort(400)



    return json.dumps(params)


if __name__ == '__main__':
    app.run()
