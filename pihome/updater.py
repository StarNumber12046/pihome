import requests
import os

r=requests.get("https://api.github.com/repos/StarNumber12046/pihome/commits", headers={"Accept": "application/vnd.github.v3+json"})


def has_updates():
  commit = r.json()[0]

  if commit["sha"] == os.popen("git rev-parse HEAD"):
    return False
  else:
    return True

def update():
  os.system("git pull")