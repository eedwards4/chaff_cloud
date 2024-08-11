# Bot to directly access URLs

from selenium import webdriver
import threading
import datetime
import random
import time
import sys

driver = webdriver.Chrome()
random.seed(time.time())

LOGGING = False

class addressBot:
    def __init__(self):
        while True:
            try:
                line = sys.stdin.readline().strip()
                if line.find("(*)"):
                    line.replace("(*)", "")
                    self.id = line
            except EOFError:
                pass
            except KeyboardInterrupt:
                break

        while True:
            try:
                line = sys.stdin.readline().strip()
                if line.find("(*)"):
                    line.replace("(*)", "")
                    self.urlSrc = line
            except EOFError:
                pass
            except KeyboardInterrupt:
                break

        self.outFileName = "{}_output".format(self.id)
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
                    break
            except EOFError:
                pass
            except KeyboardInterrupt:
                self.sigExit.release()
                work_thread.join()
                break

    def get_url(self, url):
        driver.get(url)
        if LOGGING:
            title = driver.title
            url = driver.current_url

        # Scroll down slowly (to imitate a human)
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        speed = 10
        for i in range(0, total_height, speed):
            if i > 1000:  # Long page - stop scrolling
                break
            driver.execute_script("window.scrollTo(0, {});".format(i))

    def work(self):
        outFile = open(self.outFileName, "w")
        outFile.write("Started at: {}\n".format(datetime.datetime.now()))
        while not self.sigExit.acquire(blocking=False):
            random.seed(time.time())  # Reseed random number generator on every iteration (MAY LEAD TO DUPLICATES)
            url = "https://www.google.com"
            # TODO: get random URL from source file
            self.get_url(url)
            wait_time = random.randint(10, 30)
            time.sleep(wait_time)

        outFile.write("\nStopped at: {}".format(datetime.datetime.now()))
        outFile.close()
        exit(0)

if __name__ == '__main__':
    bot = addressBot()