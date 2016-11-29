import flask as fl
from flask import Flask, Blueprint
from web.views.consumer import bp
from web import flaskconfig

app = Flask(__name__)
app.config.from_object(flaskconfig)

app.register_blueprint(bp)
