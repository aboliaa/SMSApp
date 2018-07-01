import time
import unittest

from app.validator import validate
from functionality.inbound import InboundProcessor
from functionality.outbound import OutboundProcessor
from functionality.ratelimiter import MaxLimitReachedError, RateLimiter

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_validation_correct(self):
        data = {'from': '1234567', 'to': '9876543', 'text': 'ABC'}

        raised = False
        try:
            validate(data)
        except ValueError:
            raised = True
        self.assertFalse(raised)

    def test_validation_from_incorrect(self):
        data = {'from': '12345', 'to': '9876543', 'text': 'ABC'}
        with self.assertRaises(ValueError):
            validate(data)

    def test_validation_to_incorrect(self):
        data = {'from': '1234567', 'to': '98765', 'text': 'ABC'}
        with self.assertRaises(ValueError):
            validate(data)

    def test_validation_text_missing(self):
        data = {'from': '1234567', 'to': '9876543'}
        with self.assertRaises(ValueError):
            validate(data)

    def test_inbound(self):
        inbound_data = {'from': '12345670', 'to': '98765430', 'text': 'STOP'}

        raised = False
        try:
            InboundProcessor(inbound_data).process()
        except ValueError:
            raised = True
        self.assertFalse(raised)

    def test_outbound(self):
        outbound_data = {'from': '12345671', 'to': '98765431', 'text': 'ABCD'}

        raised = False
        try:
            OutboundProcessor(outbound_data).process()
        except ValueError:
            raised = True
        self.assertFalse(raised)

    def test_optout(self):
        inbound_data = {'from': '1234567', 'to': '9876543', 'text': 'STOP'}
        outbound_data = {'from': '1234567', 'to': '9876543', 'text': 'ABCD'}

        with self.assertRaises(ValueError):
            InboundProcessor(inbound_data).process()
            OutboundProcessor(outbound_data).process()

    def test_ratelimiting_limit_reached(self):
        limiter = RateLimiter(expiry_time=2, max_items=10)

        raised = False
        for i in range(20):
            try:
                limiter.check_ratelimiting(from_num='45678901')
                i += 1
                time.sleep(.1)
            except MaxLimitReachedError:
                raised = True
                break
        self.assertTrue(raised and i == 10)

    def test_ratelimiting_limit_not_reached(self):
        limiter = RateLimiter(expiry_time=2, max_items=10)

        raised = False
        for i in range(10):
            try:
                limiter.check_ratelimiting(from_num='45678902')
                i += 1
                time.sleep(.5)
            except MaxLimitReachedError:
                raised = True
                break
        self.assertFalse(raised)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()