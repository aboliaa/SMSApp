# SMSApp: App to handle inbound and outbound SMS

This is a simple SMS app that exposes the following 2 APIs that accepts JSON data as input. 

**API /inbound/sms/  
Authentication: Basic  
Method: POST**

Input Parameters
- from (min length 6, max length 16)
- to (min length 6, max length 16)
- text (min length 1, max length 120)

Expected API behavior
- Input parameters should be valid
- When text is STOP or STOP\n or STOP\r or STOP\r\n, 
The ‘from’ and ‘to’ pair must be cached with an expiry of 4 hours.

Output JSON response:  
If required parameter is missing:  
_{"message": "", "error": "&lt;parameter_name&gt; is missing"}_
  
If parameter is invalid:  
_{"message": "", "error": "&lt;parameter_name&gt; is invalid"}_
  
Any unexpected error:  
_{"message": "", "error": "unknown failure"}_
  
If all parameters are valid:  
_{"message": "inbound sms is ok", "error": ""}_

**API /outbound/sms  
Authentication: Basic  
Method: POST**

Input Parameters

Parameter required example
- from (min length 6, max length 16)
- to (min length 6, max length 16)
- text (min length 1, max length 120)

Expected API behavior
- Input parameters should be valid
- If the pair of ‘from’ and ‘to’ matches the cached pair(STOP), return an error response with appropriate HTTP status code
(see Output JSON response below)
- Do not allow more than 50 API requests using the same ‘from’ number in 1 hour. Return an error response with
appropriate HTTP status code in case the limit has been reached (see Output JSON response below)


Output JSON response:  
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
