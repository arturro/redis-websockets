# Installation

## Redis

docker version:

* first run: `$ docker run -d -p 6379:6379 --name redis1 redis1`
* after stop/reboot: `$ docker start redis1`

## Python

* require python 3.7
* install python packages from pipfile: `$ pipenv install`

# Run

## Running the Server

To run main server you have to

* start redis `$ docker start redis1`
* run: `$ pipenv run ./ws_server.py`

## web client

Open file `web.html` in webbrowser.
On this page javascript generate a random UID and send it to server and display.

## Sending ping

To send information use `pipenv run ./redis_sender.py UID1 UID2`

This script generate:

**new**

Json with list of users to whom the notification should be sent.

For example: 
```
{
	"type": "ping",
	"uids": [1, 2, 3]
}
```
 
**old**

Json with list of users to whom the notification should be sent and a random value.
For example: 
```
{
	"type": "state",
	"value": "1",
	"uids": [1, 2, 3]
}
```

