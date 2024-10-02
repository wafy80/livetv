import os
import schedule
import time

def job():
    os.system("python3 livetv.py > livetv.log")

schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)