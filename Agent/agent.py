#!/usr/bin/env python3

import sys
import os
import requests
import json
import ast
import osquery
from sys import platform
#@="\"C:\\Anushka\\beyondc_protocol.py\" \"%1\""

# Parse the URL: beyondc://service_name?uuid=123-456-789

IP = "localhost"
args = sys.argv[1:]

if len(args) != 1:
    sys.exit(0)

# This is where you can do something productive based on the params and the
# action value in the URL. For now we'll just print out the contents of the
# parsed URL.

service_name, uuid_details = args[0].split("://", 1)[1].split("?",1)
uuid = uuid_details.split("=",1)[1].split("&")[0]
username = args[0].split("://")[1].split("?",1)[1].split("&")[1].split("=")[1]

#check platform on which agent is running

if platform == "linux" or platform == "linux2" or platform=="darwin":
    # linux and osx
    queries = ["select uid,key from authorized_keys","select name,model,uuid,size from block_devices","select name,version from chrome_extensions","select name,version from deb_packages","select name,uuid,encrypted,type from disk_encryption","select name from etc_services","select name,type,active,disabled from firefox_addons","select interface,address from interface_addresses","select interface,mac,manufacturer from interface_details","select version,device from kernel_info","select name,status from kernel_modules","select port,protocol from listening_ports","select path,type from mounts","select name,version,major,minor,patch,platform,platform_like,install_date from os_version","select vendor,version from platform_info","select processes from processes","select name,version,release from rpm_packages","select password_status,hash_alg,last_change,username from shadow","select * from system_info","select vendor,model from usb_devices","select username from users"]
    table_names = ["authorized_keys","block_devices","chrome_extensions","deb_packages","disk_encryption","etc_services","firefox_addons","interface_addresses","interface_details","kernel_info","kernel_modules","listening_ports","mounts","os_version","platform_info","processes","rpm_packages","shadow","system_info","usb_devices","users"]
    columns = [['uid', 'key'], ['name', 'model','uuid','size'], ['name', 'version'], ['name', 'version'], ['name', 'uuid','encrypted','type'], ['name'], ['name', 'type','active','disabled'], ['interface', 'address'], ['interface', 'mac','manufacturer'], ['version', 'device'], ['name', 'status'], ['port', 'protocol'], ['path', 'type'], ['name', 'version','major','minor','patch','platform','platform_like','install_date'], ['vendor', 'version'], ['processes'], ['password_status', 'hash_alg','last_change','username'], ['hostname','uuid','cpu_type','cpu_subtype','cpu_brand','cpu_physical_cores','cpu_logical_cores','cpu_microcode','physical_memory','hardware_vendor','hardware_model','hardware_version','hardware_serial','computer_name','local_hostname'], ['vendor', 'model'], ['username']]

elif platform == "win32":
    # Windows...

    columns=[['name', 'source'], ['device_id', 'encryption_method','protection_status'], ['name', 'version'], ['model', 'manufacturer','number_of_cores'], ['partitions', 'manufacturer','hardware_model','serial'], ['name'], ['name', 'version'], ['interface', 'address'], ['interface', 'mac','manufacturer'], ['version', 'device'], ['port', 'protocol'], ['user', 'type'], ['name', 'version','major','minor','patch','platform','platform_like','install_date'], ['csname', 'installed_on'], ['vendor', 'version','date'], ['processes'], ['name', 'service_type','status'], ['hostname', 'uuid','cpu_type','cpu_subtype','cpu_brand','cpu_physical_cores','cpu_logical_cores','cpu_microcode','physical_memory','hardware_vendor','hardware_model','hardware_version','hardware_serial','computer_name','local_hostname'], ['username']]
    queries = [
    	"select name,source from autoexec", #1
    	"select device_id,encryption_method,protection_status from bitlocker_info", #2
        "select name,version from chrome_extensions", #3
        "select model,manufacturer,number_of_cores from cpu_info", #4
        "select partitions,manufacturer,hardware_model,serial from disk_info", #5
        "select name from etc_services", #6
        "select name,version from ie_extensions", #7
        "select interface,address from interface_addresses", #8
        "select interface,mac,manufacturer from interface_details", #9
        "select version,device from kernel_info", #10
        "select port,protocol from listening_ports", #11
        "select user,type from logged_in_users", #12
        # "select yet to be decided from registry ", #13
        "select name,version,major,minor,patch,platform,platform_like,install_date from os_version", #14
        "select csname,installed_on from patches", #15
        "select vendor,version,date from platform_info", #16
        "select processes from processes", #17
        # "select name,version,publisher,install_date,identifying_number from programs", #18
        "select name,service_type,status from services", #19
        "select * from system_info", #20
        "select username from users" #21
        ]
    table_names = [
       
       
    	"autoexec", #1
        "bitlocker_info", #2
        "chrome_extensions", #3
        "cpu_info", #4
        "disk_info", #5
        "etc_services", #6 
        "ie_extensions", #7
        "interface_addresses", #8
        "interface_details", #9
        "kernel_info", #10
        "listening_ports", #11
        "logged_in_users", #12
        # "registry ", #13
        "os_version", #14
        "patches", #15
        "platform_info", #16
        "processes", #17
        # "programs", #18
        "services", #19
        "system_info", #20
        "users" #21
    ]

data = dict()

try:
	# Spawn an osquery process using an ephemeral extension socket.
	instance = osquery.SpawnInstance()
	instance.open()  # This may raise an exception
		
	for table,query,column in zip(table_names,queries,columns):
	# Issues queries and call osquery Thrift APIs.
		result = instance.client.query(query).response
		data[table] = dict()
		
		for col in column:
			data[table][col] = list()

		if platform == "linux" or platform == "linux2" or platform=="darwin":

			for row in result:
				for key, val in row.items(): data[table][key].append(val)
		elif platform == "win32":

			for row in result:
				for key, val in row.items(): data[table][(key.decode()).split("b'",1)[1].split("'",1)[0]].append((val.decode()).split("b'",1)[1].split("'",1)[0])

	del instance	

except Exception as e:
	print(e)

if platform == "linux" or platform == "linux2" or platform == "darwin":
	f = open("linux-data.json","w+")
	f.write(str(data))
	f.close()

	data = open("linux-data.json", 'r').read()
	data = ast.literal_eval(data)
	data = json.dumps(data)
	data = json.loads(data)
elif platform == "win32":

	f = open("windows-data.json","w+")
	f.write(str(data))
	f.close()

	data = open("windows-data.json", 'r').read()
	data = ast.literal_eval(data)
	data = json.dumps(data)
	data = json.loads(data)

data["temp_uuid"] = uuid
data["service"] = service_name
data["username"] = username

open("/tmp/write.txt","w").write(str(data))

if platform == "linux" or platform == "linux2" or platform=="darwin": json.dump(data,open("linux-final-data.json","w"))
elif platform=="win32": json.dump(data,open("windows-final-data.json","w"))



headers = {"Content-type":"application/json","Accept":"text/plain"}
r = requests.post("http://{}:9001/submit/".format(IP),data=open("linux-final-data.json","rb"),headers=headers)

print(r.text)
