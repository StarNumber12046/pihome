from flask import *
import pychromecast
import os
import socket
print(socket.gethostbyname(socket.gethostname()))

app = Flask("pihome")

env = {"src_path":"C:/Users/franc/Desktop/music", "host": "0.0.0.0", "port": "8080"}
services, browser = pychromecast.discovery.discover_chromecasts()
print(services)
print(browser)
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["GHome"])

cast = chromecasts[0]
cast.wait()
mc = cast.media_controller

def get_index(list, name):
  for a in range(len(list)):
    if list[a] == name:
      return a



@app.route("/list")
def list():
  return {"list": os.listdir(env["src_path"])}

@app.route("/")
def index():

  return render_template("index.html", np=mc.status.content_id, len = len(os.listdir(env["src_path"])), music = os.listdir(env["src_path"]))

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
  mc.next_track()
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
  mc.volume_level += 1
  return redirect("/")

@app.route("/volume-down")
def volumedown():
  mc.volume_level -= 1
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
def cast(song):
  if env["host"] == "0.0.0.0":
    host = socket.gethostbyname(socket.gethostname())
  else:
    host=env["host"]

  play=f'http://{host}:{env["port"]}/music/{song}'
  print(play)
  mc.play_media(play, 'audio/mp3')
  return redirect("/")

@app.route("/play_path", methods=['POST', 'GET'])
def play_path():
  path = request.form["path"]
  mc.play_media(f"http://{socket.gethostbyname(socket.gethostname())}:{env['port']}/play_from_path?path={path}", 'audio/mp3')
  return redirect("/")

app.run(host=env["host"], port=env["port"])