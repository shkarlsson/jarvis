# %%
from pyirobot import Robot

ip = "192.168.1.58"
password = ":1:1718021841:2HZDmiuF2noI4Ypk"
username = "3168411090527720"  # blid

import os

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# print current path
print(os.getcwd())

from app.helpers.paths import PROJECT_DIR

js_path = PROJECT_DIR / "js"

import subprocess


def control_roomba(username, password, ip):
    try:
        result = subprocess.run(
            ["node", str(js_path / "roomba.js"), username, password, ip],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        return False


control_success = control_roomba(username, password, ip)
print("Control Success:", control_success)

# %%

robot = Robot(ip, password)


robot.StartCleaning()
# %%
robot.StopCleaning()
robot.ReturnHome()
# %%
# %%
import json
from pyirobot import Robot


# %%
robot = Robot(
    ip,
    password,
)
print(robot.GetCleaningPreferences())
print(json.dumps(robot.GetCleaningPreferences(), sort_keys=True, indent=4))
# %%


import asyncio
import json
import logging
from roomba import Roomba

myroomba = Roomba(ip, username, roombaPassword, webport=8200)


# %%
# Uncomment the following two lines to see logging output
# logging.basicConfig(level=logging.INFO,
#      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# uncomment the option you want to run, and replace address, blid and password with your own values


myroomba = Roomba(ip, username, password)
# or myroomba = Roomba(address) #if you have a config file - will attempt discovery if you don't


async def test():
    myroomba.connect()
    # myroomba.set_preference("carpetBoost", "true")
    # myroomba.set_preference("twoPass", "false")

    # myroomba.send_command("start")
    # await asyncio.sleep(3)
    # print(json.dumps(myroomba.master_state, indent=2))
    # await asyncio.sleep(3)
    # myroomba.send_command("stop")
    # myroomba.send_command("dock")

    import json, time

    for i in range(3):
        print(json.dumps(myroomba.master_state, indent=2))
        await asyncio.sleep(1)
    myroomba.disconnect()


loop = asyncio.get_event_loop()
loop.run_until_complete(test())

# %%
