import jwt
from datetime import datetime, timedelta
import time

key = "KwpHfdG+hyiY3raI4YSFm4N4WOnbJY/oXWFx9DEwDnmVPU7y1S0J+wtwjyIu6kv4U2BVxiL1qv+Y4yET6Cm7Jw=="
expire = time.time() + 3
data = {"user_id": "123", "exp": expire, "role": "admin"}
encoded = jwt.encode(data, key, algorithm="HS512")
print("Enecoded: ", encoded)
decode = jwt.decode(encoded, key, algorithms="HS512")
print(type(decode))
print("Decoded: ", decode)
time.sleep(5)
time_now = time.time()
print(time_now)
if time_now > decode["exp"]:
    print("Token expired")
else:
    print("Token valid")