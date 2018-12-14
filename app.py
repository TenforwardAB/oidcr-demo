# from flask import Flask, request
# from flask_oidc import OpenIDConnect
#
# import ssl
#
# from config import Base
# import logging
# import json
#
# logging.basicConfig(filename='/tmp/ocr.log', filemode='w', level=logging.DEBUG)
#
#
# app = Flask(__name__)
# app.config.from_object(Base)
# oidc = OpenIDConnect(app)
#
#
#
# @app.route('/')
# def index():
# 	if oidc.user_loggedin:
# 		return 'Welcome %s' % oidc.user_getfield('email')
# 	else:
# 		return 'Not logged in'
#
# @app.route('/login')
# @oidc.require_login
# def login():
# 	return 'Welcome {}!! Livinig in {}'.format(oidc.user_getfield('email'), oidc.user_getfield('address'))
#
# @app.route('/custom_callback')
# @oidc.custom_callback
# def callback(data):
# 	return 'Hello. You submitted %s' % data
#
#
# if __name__ == '__main__':
# 	context = None
# 	if app.config['BASE'].startswith("https"):
# 		context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# 		context.load_cert_chain(app.config['SERVER_CERT'], app.config['SERVER_KEY'])
#
# 	app.run(ssl_context=context, host='127.0.0.1', port=8043, debug=True)

from blog import app
import ssl

if __name__ == '__main__':
	context = None
	if app.config['BASE'].startswith("https"):
		context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		context.load_cert_chain(app.config['SERVER_CERT'], app.config['SERVER_KEY'])

	app.run(ssl_context=context, host='127.0.0.1', port=8043, debug=True)