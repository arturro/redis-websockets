start redis
```
$ docker run -d -p 6379:6379 --name redis1 redis
$ docker start redis1
```


Python PUB/SUB
```
python redis_sender.py
python ws_server.py 
```