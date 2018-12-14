import subprocess
from datetime import datetime
from time import sleep
import logging


def wait_start():
    start = datetime.now()
    end = start.replace(hour=8, minute=0, second=00)
    delta = (end - start).seconds
    log.info("Next sync through: %s s", str(delta))
    sleep(delta)

def core():

    wait_start()
    sync()

def sync():
    process = subprocess.Popen('/usr/cashback/Sync.sh', shell=True, stdout=subprocess.PIPE)
    process.wait()
    core()

if __name__ == "__main__":

    log = logging.getLogger(__name__)
    format = '%(asctime)s %(levelname)s:%(message)s'
    logging.basicConfig(format=format, level=logging.INFO)
    log.info("Start sync")
    core()
