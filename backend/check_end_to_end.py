import json
import urllib.request
import sys

base = 'http://localhost:8001'

req = urllib.request.Request(
    base + '/login',
    data=json.dumps({'email': 'student@gmail.com', 'password': 'string'}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST',
)

with urllib.request.urlopen(req, timeout=20) as resp:
    body = resp.read().decode()
    print('LOGIN', resp.status)
    print(body)
    token = json.loads(body)['access_token']

p_req = urllib.request.Request(
    base + '/profile',
    headers={'Authorization': 'Bearer ' + token},
    method='GET',
)

try:
    with urllib.request.urlopen(p_req, timeout=20) as resp:
        print('PROFILE', resp.status)
        print(resp.read().decode())
except Exception as e:
    import traceback
    traceback.print_exc()
    print(type(e), e)
    sys.exit(1)
