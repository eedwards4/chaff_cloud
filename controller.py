# Botnet controller for chaff_cloud
# Created by Ethan Edwards on 8/8/24

import subprocess as sp
import threading
import random
import time
import sys

class Bot:
    def __init__(self):
        # Generate random bot id
        random.seed(time.time())
        self.id = ("" + str(random.randint(0, 9)) + str(random.randint(0, 9))
                   + str(random.randint(0, 9)) + str(random.randint(0, 9))
                   + str(random.randint(0, 9)) + str(random.randint(0, 9)))

        self.status = "idle"
        self.name = "Bot{}".format(self.id)
        self.process = None
        self.monitor_thread = None

    def start(self, botType):
        self.status = "running"
        if botType == 0:  # Start an address based bot
            try:
                self.process = sp.Popen([sys.executable, "bots/addressBot.py"], stdin=sp.PIPE)
            except Exception as e:
                print("Error starting bot: {}".format(e))
                self.status = "error"
                return
        elif botType == 1:  # Start a search based bot
            try:
                self.process = sp.Popen([sys.executable, "bots/searchBot.py"], stdin=sp.PIPE)
            except Exception as e:
                print("Error starting bot: {}".format(e))
                self.status = "error"
                return

        # Start monitor thread
        self.monitor_thread = threading.Thread(target=self.monitor)

    def monitor(self):
        # Monitor thread
        pass

    def kill(self):
        # Proper thread shutdown here
        if self.status == "running":
            self.process.stdin.write(b'kill\n')
            self.process.stdin.flush()

            # Force kill if we can't shut down gracefully
            try:
                self.process.wait(10)
            except sp.TimeoutExpired:
                print("Unable to gracefully shut down {}, force killing...".format(self.name))
                self.process.kill()
