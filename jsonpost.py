import requests
import json
import ast
data = open("/Users/chaitanyarahalkar/Downloads/without_sudo.txt", 'r').read()
final = ast.literal_eval(data)
final = json.dumps(final)
final = json.loads(final)
r = requests.post("http://localhost:8080/submit/",json=final)