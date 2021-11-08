import os, platform
if platform.system().lower() == "windows":
  
  os.system("pip install -r requirements.txt")
else:
  os.system("pip3 install -r requirements.txt")
