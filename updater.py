import requests
import os

r=requests.get("https://api.github.com/repos/StarNumber12046/pihome/commits", headers={"Accept": "application/vnd.github.v3+json"})

if not "data" in os.listdir("."):
  os.system("mkdir data")

if not "version.pihome" in os.listdir("./data"):
  os.system("git pull")
  commit = r.json()[0]
  with open("./data/version.pihome", "w") as f:
    f.write(commit["sha"])
  

def has_updates():
  commit = r.json()[0]

  with open("data/version.pihome", "r") as f:
    data = f.read()
    f.close()
  if commit["sha"] == data:
    return False
  else:
    return True

def get_changelog():
  commit = r.json()[0]
  commit = r.json()[0]
  return commit["commit"]["message"]

def update():
  os.system("git pull")
  commit = r.json()[0]
  with open("./data/version.pihome", "w") as f:
    f.write(commit["sha"])
