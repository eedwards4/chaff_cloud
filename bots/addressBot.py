# Bot to directly access urls
# Created by Ethan Edwards on 8/11/24

from selenium import webdriver
import threading
import datetime
import random
import time
import csv
import sys

driver = webdriver.Chrome()
random.seed(time.time())

class addressBot:
    def getInfo(self):
        while True:
            try:
                line = sys.stdin.readline().strip()
                if line:
                    myId = line.split(" ")[0]
                    urlSrc = line.split(" ")[1]
                    vb = int(line.split(" ")[2])
                    return myId, urlSrc, vb
            except EOFError:
                pass
            except KeyboardInterrupt:
                break

    def reader(self):
        with open(self.urlSrc, "r") as file:
            read = csv.reader(file)
            for row in read:
                self.urls.append(row[0])
            self.urls.remove(self.urls[0])

    def __init__(self):
        # Setup
        self.myId = ""
        self.urlSrc = ""
        vb = 0
        self.myId, self.urlSrc, vb = self.getInfo()
        self.verbose = False
        if vb == 1:
            self.verbose = True
        # Output file
        self.outFileName = "{}_output.txt".format(self.myId)
        self.outFile = open(self.outFileName, "w")
        # Input file
        self.urls = []
        self.reader()

        # Threading
        self.sigExit = threading.Lock()
        self.sigExit.acquire()
        work_thread = threading.Thread(target=self.work)
        work_thread.start()
        while True:
            try:
                line = sys.stdin.readline().strip()
                if line == "kill":
                    self.sigExit.release()
                    work_thread.join()
                    exit(0)
            except EOFError:
                pass
            except KeyboardInterrupt:
                self.sigExit.release()
                work_thread.join()
                exit(0)

    def get_url(self, url):
        driver.get(url)
        title = driver.title
        url = driver.current_url
        print("Accessing {} ({}) at {}".format(title, url, datetime.datetime.now()))
        self.outFile.write("Accessing {} ({}) at {}\n".format(title, url, datetime.datetime.now()))

        # Scroll down slowly (to imitate a human)
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        speed = 10
        for i in range(0, total_height, speed):
            if i > 1000:  # Long page - stop scrolling
                break
            driver.execute_script("window.scrollTo(0, {});".format(i))
            time.sleep(0.2)

    def work(self):
        print("Started at: {}".format(datetime.datetime.now()))
        self.outFile.write("Started at: {}\n".format(datetime.datetime.now()))

        for url in self.urls:
            if self.sigExit.acquire(blocking=False):
                break
            self.get_url(url)
            random.seed(time.time())
            wait_time = random.randint(10, 30)
            if self.verbose:
                print("Waiting for {} seconds".format(wait_time))
                self.outFile.write("Waiting for {} seconds\n".format(wait_time))
            time.sleep(wait_time)

        print("Stopped at: {}".format(datetime.datetime.now()))
        self.outFile.write("Stopped at: {}\n".format(datetime.datetime.now()))
        self.outFile.close()
        driver.quit()

if __name__ == '__main__':
    bot = addressBot()