from flask import Flask, render_template as rt, request, redirect, url_for
from model import *
from sqlalchemy import and_ , or_
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ \
os.path.join(current_dir,"Database.sqlite3")

db.init_app(app)
app.app_context().push() # stack in pograming

