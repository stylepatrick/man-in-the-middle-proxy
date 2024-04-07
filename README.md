# man-in-the-middle-proxy
 Proxy Server to simulate man in the middle attack with GET and POST requests.

## Victim Website
GET: http://python.vic-tim.de/images/

POST: http://python.vic-tim.de/proxy/form.html

## GET
Proxy will replace images with fake images and manipulate title of webpage.

## POST
Will proxy the POST requests if the form is filled with the message "top", it will be replaced with "flop" and send to the server. 
Original received response from server is changed that client will never now that "top" has changed to "flop".
