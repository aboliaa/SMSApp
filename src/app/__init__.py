from flask import Flask
from flask_restful import Api

from controllers import InboundSMSHandler, OutboundSMSHandler

app = Flask(__name__)
api = Api(app)

api.add_resource(InboundSMSHandler, '/inbound/sms')
api.add_resource(OutboundSMSHandler, '/outbound/sms')

