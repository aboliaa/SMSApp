import time
import requests
import unittest

def request(method, url, data=None, headers=None):
    return requests.request(method, url, data=data, headers=headers)

def get_payload(from_num, to_num, text):
    return "{\"from\": \"%s\", \"to\": \"%s\", \"text\": \"%s\"}" \
        %(from_num, to_num, text)


class Test(unittest.TestCase):
    def setUp(self):
        host = "http://127.0.0.1:5000"
        self.inbound_url = '%s/inbound/sms' %host
        self.outbound_url = '%s/outbound/sms' % host

    def test_inbound_success(self):
        from_num = '1234567'
        to_num = '9876543'
        text = 'ABC'

        payload = get_payload(from_num, to_num, text)

        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXQ="
        }

        response = request("POST", self.inbound_url, payload, headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('error',''), '')

    def test_inbound_incorrect_auth(self):
        from_num = '1234567'
        to_num = '9876543'
        text = 'ABC'

        payload = get_payload(from_num, to_num, text)

        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXW="
        }

        response = request("POST", self.inbound_url, payload, headers)

        self.assertEqual(response.status_code, 401)

    def test_inbound_input_missing(self):
        to_num = '9876543'
        text = 'ABC'

        payload = "{\"to\": \"%s\", \"text\": \"%s\"}" \
        % (to_num, text)

        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXQ="
        }

        response = request("POST", self.inbound_url, payload, headers)

        self.assertEqual(response.status_code, 200)
        error = response.json().get('error', '')
        expected = 'from is missing'
        self.assertEqual(error, expected)

    def test_inbound_input_invalid(self):
        from_num = '12345'
        to_num = '9876543'
        text = 'ABC'

        payload = get_payload(from_num, to_num, text)

        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXQ="
        }

        response = request("POST", self.inbound_url, payload, headers)

        self.assertEqual(response.status_code, 200)
        error = response.json().get('error', '')
        expected = 'from is invalid'
        self.assertEqual(error, expected)

    def test_opt_out(self):
        from_num = '1234567'
        to_num = '9876543'
        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXQ="
        }

        text = 'STOP'
        payload = get_payload(from_num, to_num, text)
        response = request("POST", self.inbound_url, payload, headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('error', ''), '')

        text = 'ABCD'
        payload = get_payload(from_num, to_num, text)
        response = request("POST", self.outbound_url, payload, headers)
        self.assertEqual(response.status_code, 200)
        error = response.json().get('error', '')
        expected = 'sms from %s and to %s blocked by STOP request' %(from_num, to_num)
        self.assertEqual(error, expected)

    def test_outbound_ratelimiting_limit_reached(self):
        from_num = '12345671228'
        to_num = '98765432'
        text = 'ABC'

        payload = get_payload(from_num, to_num, text)

        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXQ="
        }

        for i in range(51):
            response = request("POST", self.outbound_url, payload, headers)

        self.assertEqual(response.status_code, 200)

        error = response.json().get('error', '')
        expected = 'Limit reached for from %s' %from_num
        self.assertEqual(error, expected)

    def test_outbound_ratelimiting_limit_not_reached(self):
        from_num = '12345671238'
        to_num = '98765432'
        text = 'ABC'

        payload = get_payload(from_num, to_num, text)

        headers = {
            'content-type': "application/json",
            'authorization': "Basic dXNlcjpzZWNyZXQ="
        }

        for i in range(50):
            response = request("POST", self.outbound_url, payload, headers)

        self.assertEqual(response.status_code, 200)

        error = response.json().get('error', '')
        expected = ''
        self.assertEqual(error, expected)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
