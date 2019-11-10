#!/usr/bin/env python

import sys
import urllib.parse
import os
import requests
import json
import ast
import osquery
#@="\"C:\\Anushka\\beyondc_protocol.py\" \"%1\""

if len(args) != 1:
    return 1

# Parse the URL: beyondc://service_name?uuid=123-456-789

service_name, uuid_details = args[0].split("://", 1)[1].split("?",1)
uuid = uuid_details.split("=",1)[1]

# This is where you can do something productive based on the params and the
# action value in the URL. For now we'll just print out the contents of the
# parsed URL.


#os.system(params['uuid'][0])

queries = ["select uid,key from authorized_keys","select name,model,uuid,size from block_devices","select name,version from chrome_extensions","select name,version from deb_packages","select name,uuid,encrypted,type from disk_encryption","select name from etc_services","select name,type,active,disabled from firefox_addons","select interface,address from interface_addresses","select interface,mac,manufacturer from interface_details","select version,device from kernel_info","select name,status from kernel_modules","select port,protocol from listening_ports","select path,type from mounts","select name,version,major,minor,patch,platform,platform_like,install_date from os_version","select vendor,version from platform_info","select processes from processes","select name,version,release from rpm_packages","select password_status,hash_alg,last_change,username from shadow","select * from system_info","select vendor,model from usb_devices","select username from users"]
table_names = ["authorized_keys","block_devices","chrome_extensions","deb_packages","disk_encryption","etc_services","firefox_addons","interface_addresses","interface_details","kernel_info","kernel_modules","listening_ports","mounts","os_version","platform_info","processes","rpm_packages","shadow","system_info","usb_devices","users"]
data = dict()

# Spawn an osquery process using an ephemeral extension socket.
instance = osquery.SpawnInstance()
instance.open()  # This may raise an exception
for table,query in zip(table_names,queries):
# Issues queries and call osquery Thrift APIs.
        data[table] = instance.client.query(query).response

f = open("data.json","w+")
f.write(str(data))
f.close()
data = open("data.json", 'r').read()
final = ast.literal_eval(data)
final = json.dumps(final)
final = json.loads(final)
final["uuid"] = uuid
final["service"] = service_name
r = requests.post("http://localhost:9001/submit/",json=final)


# beyondc://action?uuid=


