from flask import Flask, request
from flask_oidc import OpenIDConnect

from flaskext.markdown import Markdown

from config import Base
import logging
import json

logging.basicConfig(filename='/tmp/ocr.log', filemode='w', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Base)
Markdown(app)
oidc = OpenIDConnect(app)

from blog import models  # noqa
from blog import views  # noqa

