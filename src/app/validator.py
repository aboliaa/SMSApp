from marshmallow import Schema, fields, ValidationError, post_load
from marshmallow.validate import Length
from utils.log import logger

__all__ = ['validate']

class ResourceSchema(Schema):
    from_num = fields.Str(
        load_from='from',
        dump_to='from',
        required=True,
        validate=Length(
            min=6,
            max=16,
            error='from is invalid'
        ),
        error_messages={
            'required': 'from is missing',
            'validator_failed': 'from is invalid',
            'type': 'from is invalid'
        }
    )

    to = fields.Str(
        required=True,
        validate=Length(
            min=6,
            max=16,
            error='to is invalid'
        ),
        error_messages={
            'required': 'to is missing',
            'validator_failed': 'to is invalid',
            'type': 'to is invalid'
        }
    )

    text = fields.Str(
        required=True,
        error_messages={
            'required': 'text is missing',
            'validator_failed': 'text is invalid',
            'type': 'text is invalid'
        }
    )

    class Meta:
        strict = True


def validate(data):
    validation_schema = ResourceSchema()

    try:
        validation_schema.load(data)
    except ValidationError as e:
        logger.debug('Error messages are: %s' %str(e))
        try:
            error_message = e.messages.values()[0][0]
        except Exception as e:
            logger.error(str(e))
            error_message = 'unknown failure'
        raise ValueError(error_message)

