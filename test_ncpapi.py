#!/usr/bin/python3
# -*- coding: utf-8 -*-



# -------------------------------------------------------------------
# Purpose: Naver Cloud Platform APIs Test
# Author: Ho-Jung Kim (godmode2k@hotmail.com)
# Filename: test_ncpapi.py
# Date: Since October 25, 2021
#
#
# Reference:
# - https://api.ncloud-docs.com/beta/docs/common-ncpapi#
# - https://api.ncloud-docs.com/beta/docs/management-monitoring-getmetricstatisticlist
# - https://github.com/NaverCloudPlatform/ncloud-sdk-python
#
#
# Note:
# - USE THIS AT YOUR OWN RISK
#
#
# License:
#
#*
#* Copyright (C) 2021 Ho-Jung Kim (godmode2k@hotmail.com)
#*
#* Licensed under the Apache License, Version 2.0 (the "License");
#* you may not use this file except in compliance with the License.
#* You may obtain a copy of the License at
#*
#*      http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software
#* distributed under the License is distributed on an "AS IS" BASIS,
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#* See the License for the specific language governing permissions and
#* limitations under the License.
#*
# -------------------------------------------------------------------

import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json

from datetime import datetime, timezone, timedelta

import threading
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


'''
$ cat $HOME/.ncloud/configure
NCLOUD_ACCESS_KEY_ID={access-key}
NCLOUD_SECRET_KEY={secret-key}
ncloud_access_key_id={access-key}
ncloud_secret_access_key={secret-key}


https://ncloud.apigw.ntruss.com/monitoring/v2/getMetricStatisticList?responseFormatType=json

POST /monitoring/v2/getMetricStatisticList?responseFormatType=json HTTP/1.1
Host: 127.0.0.1:9999
Accept-Encoding: identity
Content-Length: 142
Content-Type: application/x-www-form-urlencoded
User-Agent: Swagger-Codegen/1.1.6/python
x-ncp-apigw-timestamp: {timestamp}
x-ncp-iam-access-key: {access-key}
x-ncp-apigw-signature-v1: {sign-key}

instanceNoList.1=<instance number>&metricName=DiskWriteBytes&startTime=2021-10-28T00%3A00%3A00%2B0900&endTime=2021-10-28T02%3A00%3A00%2B0900&period=1800
'''



# ------------------------------------------------------
# NCP API
# ------------------------------------------------------
class CNCP_API_Monitor():
    def __init__(self):
        pass

    # ------------------------------------
    # ------------------------------------
    def make_signature(self, timestamp, access_key, secret_key):
        method = "POST"
        uri = "/monitoring/v2/getMetricStatisticList?responseFormatType=json"
        #uri = "/monitoring/v2/getListMetrics?responseFormatType=json"

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        print( "message = " + message )
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    # ------------------------------------
    # ------------------------------------
    def ncp_api_v2_getMetricStatisticList(self, ACCESS_KEY, SECRET_KEY, INSTANCE_NO, METRIC_NAME, TIME_START, TIME_END):
        TIMESTAMP = int(time.time() * 1000)
        TIMESTAMP = str( TIMESTAMP )

        # test
        '''
        timestamp = int(time.time() * 1000)
        timestamp = time.time()
        utc = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print( "UTC = " + str(utc) )
        timestamp = str( timestamp )

        #timestamp = datetime.now() + timedelta(hours=9)
        #timestamp = timestamp.timestamp()
        #dt_9 = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        #print( "UTC+9 dt_9 = " + str(dt_9) )
        '''

        # test
        '''
        #timestamp = time.time()

        #tz = timezone(timedelta(hours=9))
        #dt_9 = datetime.fromtimestamp(timestamp, tz)
        #dt_9 = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%s')
        #timestamp = datetime.timestamp( datetime.strptime(dt_9, '%Y-%m-%d %H:%M:%S') )
        #print( "dt_9 = " + str(timestamp) )
        #timestamp = datetime.now(timezone.utc).timestamp()
        '''

        # DateTime format
        # startTime: "2021-10-27T00:00:00+0900"
        # endTime:   "2021-10-28T00:00:00+0900"



        SIGNKEY = self.make_signature( TIMESTAMP, ACCESS_KEY, SECRET_KEY )
        print( SIGNKEY )
        SIGNKEY = str( SIGNKEY.decode("utf-8") )
        print( "sign_key = " + SIGNKEY )
        print( "timestamp = " + TIMESTAMP )
        print( "access_key = " + ACCESS_KEY )


        URL = "https://ncloud.apigw.ntruss.com/monitoring/v2/getMetricStatisticList?responseFormatType=json"
        #URL = "https://ncloud.apigw.ntruss.com/monitoring/v2/getListMetrics?responseFormatType=json"


        #headers = { 'Content-Type':'application/json; charset=utf-8; application/x-www-form-urlencoded',
        #headers = { 'Content-Type':'application/json; charset=utf-8',
        headers = { 
            'Content-Type':'application/x-www-form-urlencoded',
            "x-ncp-apigw-timestamp": TIMESTAMP,
            #"x-ncp-apigw-api-key": "",
            "x-ncp-iam-access-key": ACCESS_KEY,
            #"x-ncp-apigw-signature-v2": SIGNKEY
            "x-ncp-apigw-signature-v1": SIGNKEY
            }

        data = { "instanceNoList.1": INSTANCE_NO,
                 "metricName": METRIC_NAME,
                 #"startTime": "2021-10-27T00:00:00+0900",
                 #"endTime": "2021-10-28T00:00:00+0900",
                 "startTime": TIME_START,
                 "endTime": TIME_END, 
                 "period": 1800
               }
        #data = { "instanceNo": INSTANCE_NO }



        #print( headers )
        res = requests.post( URL, data = data, headers = headers )
        #print( "res code = " + str(res.status_code) )
        #print( "response = \n" + res.text )
        return res


        # DO NOT USE THIS:
        # example
        '''
        curl -i -X GET \
                -H "x-ncp-apigw-timestamp:1505290625682" \
                -H "x-ncp-iam-access-key:D78BB444D6D3C84CA38D" \
                -H "x-ncp-apigw-signature-v2:WTPItrmMIfLUk/UyUIyoQbA/z5hq9o3G8eQMolUzTEa=" \
                'https://example.apigw.ntruss.com/photos/puppy.jpg?query1=&query2'
        '''

    # ------------------------------------
    # Test
    # ------------------------------------
    def test(self):
        #INSTANCE_NO = "<instance number>"
        INSTANCE_NO = "1234"


        #METRIC_NAME = "DiskWriteBytes"
        METRIC_NAME = "CPUUtilization"


        # DateTime format
        #start: "2021-10-27T00:00:00+0900"
        #end:   "2021-10-28T00:00:00+0900"

        TIME_START = "2021-10-27T00:00:00+0900"
        TIME_END = "2021-10-28T00:00:00+0900"

        #timestamp = time.time()
        #TIME_START = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S+0900')
        #TIME_END = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S+0900')

        # Keys
        ACCESS_KEY = "<ACCESS_KEY>"
        SECRET_KEY = "<SECRET_KEY>"
        SECRET_KEY = bytes(SECRET_KEY, 'UTF-8')


        self.ncp_api_v2_getMetricStatisticList( ACCESS_KEY, SECRET_KEY, INSTANCE_NO, METRIC_NAME, TIME_START, TIME_END )



# ------------------------------------------------------
# JSON-RPC Server
#
# $ pip install jsonrpclib
#
# test
# $ curl -X POST --data '{"jsonrpc":"2.0","method":"ncp_monitor","params":[],"id":0}' -H "Content-Type: application/json" http://127.0.0.1:8888/
# ------------------------------------------------------
class CJSONRPCServer():
    def __init__(self):
        pass

    def rpc_call_test(self):
        result = "test_call"
        #return json.dumps(result).encode("utf-8")
        return '{"result": "' + result + '"}'

    def rpc_call_ncp_monitor(self):
        #INSTANCE_NO = "<instance number>"
        INSTANCE_NO = "1234"

        #METRIC_NAME = "DiskWriteBytes"
        METRIC_NAME = "CPUUtilization"

        # DateTime format
        #start: "2021-10-27T00:00:00+0900"
        #end:   "2021-10-28T00:00:00+0900"

        TIME_START = "2021-10-27T00:00:00+0900"
        TIME_END = "2021-10-28T00:00:00+0900"

        #timestamp = time.time()
        #TIME_START = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S+0900')
        #TIME_END = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S+0900')
        #print( utc )

        # Keys
        ACCESS_KEY = "<ACCESS_KEY>"
        SECRET_KEY = "<SECRET_KEY>"
        SECRET_KEY = bytes(SECRET_KEY, 'UTF-8')
  

        monitor = CNCP_API_Monitor()
        result = monitor.ncp_api_v2_getMetricStatisticList( ACCESS_KEY, SECRET_KEY, INSTANCE_NO, METRIC_NAME, TIME_START, TIME_END )
        #print( "res code = " + str(res.status_code) )
        #print( "response = \n" + res.text )
        res = {}
        res["code"] = str( result.status_code )
        res["response"] = json.loads( str(result.text ) )

        #result = {}
        #result["result"] = res
        #json.dumps(result).encode("utf8")
        #return result
        return res

    def run_jsonrpc_server(self):
        print( "JSON-RPC Server starting..." )
        server = SimpleJSONRPCServer( ('0.0.0.0', 8888) )

        server.register_function( self.rpc_call_test, "test" )
        server.register_function( self.rpc_call_ncp_monitor, "ncp_monitor" )
        #server.register_function( lambda x, y: x + y, 'add' )

        print( "running..." )
        server.serve_forever()



# ------------------------------------------------------
# ------------------------------------------------------
if __name__ == "__main__":
    # JSON-RPC
    rpc_server = CJSONRPCServer()
    th_jsonrpc = threading.Thread( target = rpc_server.run_jsonrpc_server )
    th_jsonrpc.start()
    th_jsonrpc.join()


