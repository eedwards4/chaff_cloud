# Botnet controller for chaff_cloud
# Created by Ethan Edwards on 8/8/24

import subprocess as sp
import threading
import random
import time
import sys

class Bot:
    def __init__(self, _src, _verbose, _type):
        # Generate random bot id
        random.seed(time.time())
        self.id = ("" + str(random.randint(0, 9)) + str(random.randint(0, 9))
                   + str(random.randint(0, 9)) + str(random.randint(0, 9))
                   + str(random.randint(0, 9)) + str(random.randint(0, 9)))

        self.src = _src
        self.verbose = _verbose
        self.botType = _type
        self.status = "idle"
        self.name = "Bot{}".format(self.id)
        self.process = None
        self.monitor_thread = None

    def start(self):
        self.status = "running"
        if self.botType == 0:  # Start an address based bot
            try:
                self.process = sp.Popen([sys.executable, "bots/addressBot.py"], stdin=sp.PIPE)
            except Exception as e:
                print("Error starting bot: {}".format(e))
                self.status = "error"
                return
        elif self.botType == 1:  # Start a search based bot
            try:
                self.process = sp.Popen([sys.executable, "bots/searchBot.py"], stdin=sp.PIPE)
            except Exception as e:
                print("Error starting bot: {}".format(e))
                self.status = "error"
                return

        # Start monitor thread
        self.monitor_thread = threading.Thread(target=self.monitor)
        self.monitor_thread.start()

    def monitor(self):
        # Monitor thread
        self.process.stdin.write('{} {} {}\n'.format(self.id, self.src, self.verbose).encode())
        self.process.stdin.flush()
        pass

    def kill(self):
        # Proper thread shutdown here
        if self.status == "running":
            self.process.stdin.write(b'kill\n')
            self.process.stdin.flush()

            # Force kill if we can't shut down gracefully after 60 seconds
            try:
                self.process.wait(60)
            except sp.TimeoutExpired:
                print("Unable to gracefully shut down {}, force killing...".format(self.name))
                self.process.kill()
            self.monitor_thread.join()
            self.status = "killed"
        else:
            print("Bot {} has status: {}".format(self.name, self.status))

def main():
    # Botnet controller
    bots = []
    while True:
        line = input("Enter command: ")
        if line == "new":
            botType = int(input("Bot type (0=address, 1=search): "))
            src = input("Enter name of source file: ")
            verbose = 1 if input("Verbose? (y/n): ").lower() == "y" else 0
            if botType == 0:
                bots.append(Bot(src, verbose, 0))
            elif botType == 1:
                bots.append(Bot(src, verbose, 1))
            else:
                print("Invalid bot type!")
        elif line == "start":
            target = input("Enter bot name: ")
            for bot in bots:
                if bot.name == target:
                    bot.start()
        elif line == "list":
            for bot in bots:
                print("{} ({})".format(bot.name, bot.status))
        elif line == "kill":
            target = input("Enter bot name: ")
            for bot in bots:
                if bot.name == target:
                    bot.kill()
        elif line == "quit":
            for bot in bots:
                bot.kill()
            exit(0)

if __name__ == '__main__':
    main()
