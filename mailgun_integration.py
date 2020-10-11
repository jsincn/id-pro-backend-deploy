import requests
from flask import render_template
import os


def send_email(email, id):

    template = render_template("emailFirstContact.html", id_val=id)
    return requests.post(
        "https://api.eu.mailgun.net/v3/mg.stei.ml/messages",
        auth=("api", os.environ.get("mailgun-id-pro")),
        data={"from": "ID <no-reply@mg.stei.ml>",
              "to": [email],
              "subject": "Your ID-PRO code",
              "text": "Ihre ID ist: " + str(id) + "- An einem sicheren Ort aufbewahren! - Privacy: https://stei.ml/privacy "
                                             "- "
                                             "Info: https://stei.ml/info",
              "html": template})


def send_recovery_email(email, id):

    template = render_template("emailRecovery.html", id_val=id)
    return requests.post(
        "https://api.eu.mailgun.net/v3/mg.stei.ml/messages",
        auth=("api",  os.environ.get("mailgun-id-pro")),
        data={"from": "ID <no-reply@mg.stei.ml>",
              "to": [email],
              "subject": "Your ID-PRO code",
              "text": "Ihre ID ist: " + str(id) + "- An einem sicheren Ort aufbewahren! - Privacy: https://stei.ml/privacy "
                                             "- "
                                             "Info: https://stei.ml/info",
              "html": template})
