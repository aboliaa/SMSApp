# SMSApp 
App to handle inbound and outbound SMS  
This is a simple SMS app that exposes the following 2 APIs that accepts JSON data as input. 

## Architecture
- This app is written in Python using Flask web framework.  
- Caching and Ratelimiting is implemented by maintaining required information in Redis.  
- User data (credentials) are stored in SQLite.

## Installation

Install all required Python packages using requirements.txt
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Install and run Redis server by following these steps:

[https://redis.io/topics/quickstart](https://redis.io/topics/quickstart)

OR  
[https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04)  
Note that, default port for Redis is 6379. If your Redis server is running at different port, change it in config.py.

## Running the server
This is a Python Flask server. Use script run.py to run the server locally.

```
python run.py
```
You can access the server at ```http://127.0.0.1:5000/```

Test user is already populated in sqlite database. Credentials user:secret can be used for Basic authentication.

## Running the tests
Run the unit tests using following script
```
python tests/unittests.py
python tests/integration.py
```

## API specification

### Inbound SMS

URL: /inbound/sms/  
Authentication: Basic  
Method: POST

#### Input Parameters
- from (min length 6, max length 16)
- to (min length 6, max length 16)
- text (min length 1, max length 120)

#### Expected API behavior
- Input parameters should be valid
- When text is STOP or STOP\n or STOP\r or STOP\r\n, 
The ‘from’ and ‘to’ pair must be cached with an expiry of 4 hours.

#### Output JSON response:  
If required parameter is missing:  
_{"message": "", "error": "&lt;parameter_name&gt; is missing"}_
  
If parameter is invalid:  
_{"message": "", "error": "&lt;parameter_name&gt; is invalid"}_
  
Any unexpected error:  
_{"message": "", "error": "unknown failure"}_
  
If all parameters are valid:  
_{"message": "inbound sms is ok", "error": ""}_


### Outbound SMS

URL: /outbound/sms/  
Authentication: Basic  
Method: POST

#### Input Parameters

Parameter required example
- from (min length 6, max length 16)
- to (min length 6, max length 16)
- text (min length 1, max length 120)

#### Expected API behavior
- Input parameters should be valid
- If the pair of ‘from’ and ‘to’ matches the cached pair(STOP), return an error response with appropriate HTTP status code
(see Output JSON response below)
- Do not allow more than 50 API requests using the same ‘from’ number in 1 hour. Return an error response with
appropriate HTTP status code in case the limit has been reached (see Output JSON response below)


#### Output JSON response:  
If required parameter is missing:  
_{"message": "", "error": "&lt;parameter_name&gt; is missing"}_
  
If parameter is invalid:  
_{"message": "", "error": "&lt;parameter_name&gt; is invalid"}_

If the pair ‘to’ and ‘from’ matches the cached pair:  
_{"message": "", "error": "sms from &lt;from&gt; and to &lt;to&gt; blocked by STOP request"}_  

If 50 requests limit reached in last 1 hour with same ‘from’ parameter:  
_{"message": "", "error": "limit reached for from &lt;from&gt;"}_
  
Any unexpected error:  
_{"message": "", "error": "unknown failure"}_
  
If all parameters are valid:  
_{"message": "inbound sms is ok", "error": ""}_
