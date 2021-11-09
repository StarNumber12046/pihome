from flask import *
import pychromecast
import os
import socket
import json
import updater
import dotenv
import colorama
from colorama import Fore, Back, Style
print(socket.gethostbyname(socket.gethostname()))

colorama.init()

if not "config.json" in os.listdir("."):
  print("Config file not found. Creating one...")
  with open("config.pihome", "r") as f:
    default_conf = f.read()
    f.close
  with open("config.json", "w") as f:
    f.write(default_conf)
    f.close()

if updater.has_updates():
  print(colorama.Fore.RED + "Updates available!" + colorama.Style.RESET_ALL)
  print("Press W+Enter to see the changelog, U+Enter to update and C+Enter to cancel")
  ch1 = input("> ")
  if ch1.lower() == "w":
    print(updater.get_changelog())
    ch = input("Do you want to update? (y/n)\n[y]> ")
    if ch.lower() == "y":
      updater.update()
      print("Update successful")
    elif ch.lower() == "n":
      print("Update cancelled")
    else:
      updater.update()
      print("Update succesfull")
  if ch1.lower() == "u":
    updater.update()
  elif ch1.lower() == "c":
    print("Update cancelled")
  
  

app = Flask("pihome")
f = open("config.json", "r")

env = json.load(f)
print(env)
f.close()

if env["ip_override"] == "None":
  env["ip_override"] = socket.gethostbyname(socket.gethostname())
try:
  services, browser = pychromecast.discovery.discover_chromecasts()
  print(services)
  print(browser)
  chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["GHome"])

  cast = chromecasts[0]
  cast.wait()
  mc = cast.media_controller
except:
  exit("No chromecast found")

def get_index(list, name):
  for a in range(len(list)):
    if list[a] == name:
      return a



@app.route("/list")
def list():
  return {"list": sorted(os.listdir(env["src_path"]))}

@app.route("/")
def index():

  return render_template("index.html", np=mc.status.content_id, len = len(os.listdir(env["src_path"])), music = sorted(os.listdir(env["src_path"])))

@app.route("/music/<track>")
def music(track):
  return send_file(env["src_path"] + "/" + track)

@app.route("/pause")
def pause():
  mc.pause()
  return redirect("/")

@app.route("/play")
def play():
  mc.play()
  return redirect("/")

@app.route("/next")
def next():
  if mc.status.content_id is None:
    mc.play_media(env["src_path"] + "/" + os.listdir(env["src_path"])[0], "audio/mp3")
  if not mc.status.content_id.startswith("http"):
    
    mc.next_track()
  else:
    try:
      song = mc.status.content_id[32:]
      list = os.listdir(env["src_path"])
      print(get_index(list, song))
      mc.play_media(env["src_path"] + "/" + list[get_index(list, song)+1], "audio/mp3")
    except:
      mc.play_media(env["src_path"] + "/" + os.listdir(env["src_path"])[0], "audio/mp3")
  return redirect("/")

@app.route("/prev")
def prev():
  mc.previous_track()
  return redirect("/")

@app.route("/stop")
def stop():
  mc.stop()
  return redirect("/")

@app.route("/volume/<vol>")
def volume(vol):
  mc.volume = int(vol)
  return redirect("/")

@app.route("/volume-up")
def volumeupp():
  cast.set_volume(cast.status.volume_level + 0.1)
  return redirect("/")

@app.route("/volume-down")
def volumedown():
  cast.set_volume(cast.status.volume_level - 0.1)
  return redirect("/")

@app.route("/loop")
def loop():
  print(mc.repeat)
  if mc.repeat:
    mc.repeat = True
  else:
    mc.repeat = False
  return redirect("/")

@app.route("/play_from_path/")
def play_from_path():
  path = request.args.get("path")
  return send_file(path)

@app.route("/cast/<song>")
def start_song(song):
  host = env["ip_override"]

  play=f'http://{host}:{env["port"]}/music/{song}'
  print(play)
  mc.play_media(play, 'audio/mp3')
  return redirect("/")

@app.route("/play_path", methods=['POST', 'GET'])
def play_path():
  path = request.form["path"]
  mc.play_media(f"http://{env['ip_override']}:{env['port']}/play_from_path?path={path}", 'audio/mp3')
  return redirect("/")

app.run(host=env["host"], port=env["port"])
