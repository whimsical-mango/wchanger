import requests
import random
import ctypes
import os
import subprocess as sp
import sys

image_exists = sp.run(["powershell.exe", "-Command", "Get-ChildItem image* 2>$null"], shell=True, capture_output=True, text=True)
file_exist = bool(image_exists.stdout.strip())

if file_exist == True:
    sp.run(["powershell.exe", "-Command", "Remove-Item", "image*"], shell=True)

class Wallpaper:
    """Starting Variables"""
    def __init__(self):
        # Public collection's location and Main URLs
        if len(sys.argv) > 1:
            self.c_url = f"https://wallhaven.cc/api/v1/collections/{sys.argv[1]}"

        self.url = ""

        # Json data
        self.data = ""

    """Gettings Items from a collection"""
    def get_items(self):
        # Get request
        response = requests.get(self.c_url)
        # Checking the response
        if response.status_code == 200:
            self.data = response.json()
        else:
            print(f"Request failed with the status code: {response.status_code}")

    """Selecting a random wallpaper"""
    def random_wall(self):
        r_wall = random.choice(self.data["data"])
        filetype = r_wall["file_type"]
        self.filename = "image." + filetype.removeprefix("image/")
        url = r_wall["path"]
  
        # Downloading the wall
        response = requests.get(url)
        with open(self.filename, "wb") as file:
            file.write(response.content)

    def set_wall(self):
        # Constants
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDWININICHANGE = 0x02
        
        # Path
        image_path = os.path.abspath(self.filename)

        # Set the wallpaper
        ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )   


wall = Wallpaper()
wall.get_items()
wall.random_wall()
wall.set_wall()
