from flask import Flask, request
from flask_restful import Resource, Api

from validator import validate

app = Flask(__name__)
api = Api(app)

class InboundSMSHandler(Resource):
    def post(self):
        message = ''
        error = ''

        data = request.get_json() or {}
        print 'Input for inbound sms: %s' %data

        try:
            validate(data)
        except Exception as e:
            error = str(e)

        return dict(message=message, error=error)


class OutboundSMSHandler(Resource):
    def post(self):
        message = ''
        error = ''

        data = request.get_json() or {}
        print 'Input for inbound sms: %s' %data

        try:
            validate(data)
        except Exception as e:
            error = str(e)

        return dict(message=message, error=error)


api.add_resource(InboundSMSHandler, '/inbound/sms')
api.add_resource(OutboundSMSHandler, '/outbound/sms')

if __name__ == '__main__':
    app.run()
