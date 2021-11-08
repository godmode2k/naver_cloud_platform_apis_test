#!/usr/bin/python3
# -*- coding: utf-8 -*-



# -------------------------------------------------------------------
# Purpose: Naver Cloud Platform APIs Test
# Author: Ho-Jung Kim (godmode2k@hotmail.com)
# Filename: test_ncpapi_test.py
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

import requests
import json



# Test
# $ curl -X POST --data '{"jsonrpc":"2.0","method":"ncp_monitor","params":[],"id":0}' -H "Content-Type: application/json" http://127.0.0.1:8888/


if __name__ == "__main__":
    URL = "http://127.0.0.1:8888"
    DATA = {
        "id":0,
        "jsonrpc": "2.0",
        "method": "ncp_monitor",
        "params": []
    }
    HEADERS = { 'Content-Type':'application/json; charset=utf-8' }
    DATA = json.dumps( DATA )
    res = requests.post( URL, data = DATA, headers = HEADERS )

    print( "res code = " + str(res.status_code) )
    print( "response = \n" + res.text )
    print( json.loads(res.text) )

