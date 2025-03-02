#!/usr/bin/env python

import requests
import shutil
import time
import sys

BASEURL = 'http://192.168.107.1/osc/'


resp = requests.get(BASEURL + 'info')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /osc/info/ {}'.format(resp.status_code))

# Start Session
data = {"name": "camera.startSession", "parameters": {}}
resp = requests.post(BASEURL + 'commands/execute', json=data)
resp.raise_for_status()
session_id = resp.json()["results"]["sessionId"]
print(f"SessionId: {session_id}")


data = {"name": "camera.startSession", "parameters": {}}
resp = requests.post(BASEURL + 'commands/execute', json=data)
resp.raise_for_status()
picture_id = resp.json()["id"]
print("Click!")

# Wait for Processing
sys.stdout.write("Waiting for image processing")
sys.stdout.flush()
for _ in range(30):
    sys.stdout.write(".")
    sys.stdout.flush()
    data = {"id": picture_id}
    resp = requests.post(BASEURL + 'commands/status', json=data)
    resp.raise_for_status()
    if resp.json()["state"] == "done":
        break
    time.sleep(0.5)
print()

uri = resp.json()["results"]["fileUri"]

# Download Image
print(f"Downloading image: {uri}")
data = {"name": "camera.getImage", "parameters": {"fileUri": uri}}
resp = requests.post(BASEURL + 'commands/execute', json=data, stream=True)
resp.raise_for_status()
image_name = f"OSC_{picture_id}.JPG"
with open(image_name, 'wb') as ofh:
    for chunk in resp.iter_content(chunk_size=8192):
        ofh.write(chunk)
print(f"Image stored as: {image_name}")
