from flask import request
from flask_restful import Resource

from validator import validate
from functionality.inbound import InboundProcessor
from functionality.outbound import OutboundProcessor
from utils.log import logger

class InboundSMSHandler(Resource):
    def post(self):
        message = ''
        error = ''

        data = request.get_json() or {}
        logger.info('Input for inbound sms: %s' %data)

        try:
            validate(data)
            InboundProcessor(data).process()
            message = 'inbound sms is ok'
        except Exception as e:
            error = str(e) or 'unknown failure'

        return dict(message=message, error=error)


class OutboundSMSHandler(Resource):
    def post(self):
        message = ''
        error = ''

        data = request.get_json() or {}
        logger.info('Input for outbound sms: %s' %data)

        try:
            validate(data)
            OutboundProcessor(data).process()
            message = 'outbound sms is ok'
        except Exception as e:
            error = str(e) or 'unknown failure'
            logger.error(error)

        return dict(message=message, error=error)
