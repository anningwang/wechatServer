# -*- coding: utf-8 -*-
#  filename: __init__.py

from apscheduler.schedulers.background import BackgroundScheduler
import basic
import threading


__q = threading.Lock()        # create a lock object
__token = basic.Basic()
scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', id='job_id_wx_token', seconds=2)
def job_function():
    __q.acquire()  # acquire the lock
    __token.run(2)
    __q.release()  # release the lock


scheduler.start()


def get_access_token_for_wx():
    __q.acquire()
    __token.get_access_token()
    __q.release()
