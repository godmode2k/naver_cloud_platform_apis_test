# Naver Cloud Platform APIs Test


Summary
----------
> Naver Cloud Platform APIs Test: </br>
> Monitoring APIs test </br>


Environment
----------
> build all and tested on GNU/Linux

    GNU/Linux: Ubuntu 20.04_x64 LTS
    Python: v3.x


Run
----------
```sh
INSTANCE_NO = "1234"
ACCESS_KEY = "<ACCESS_KEY>"
SECRET_KEY = "<SECRET_KEY>"

METRIC_NAME = "CPUUtilization"
TIME_START = "2021-10-27T00:00:00+0900"
TIME_END = "2021-10-28T00:00:00+0900"


// Start JSON-RPC Server (http://127.0.0.1:8888)
$ python3 ./test_ncpapi.py

// Request
$ python3 ./test_ncpapi_test.py
or
$ curl -X POST --data '{"jsonrpc":"2.0","method":"ncp_monitor","params":[],"id":0}' -H "Content-Type: application/json" http://127.0.0.1:8888/

```
