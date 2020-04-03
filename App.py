from flask import Flask,render_template, request
from durable.lang import *


app = Flask(__name__)
app.debug  = True
app.static_folder = 'static'
