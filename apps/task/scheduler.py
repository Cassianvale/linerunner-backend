# -*-coding:utf-8 -*-


from apscheduler.schedulers.background import BackgroundScheduler
from ..case.run_case import run_case,run_case_test,run_case_list
from ..generateCase.run_case import run_case_task
import json
import logging
import os
from datetime import datetime
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_PATH, '../log/scheduler_log.txt')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_path,
                    filemode='a')
_scheduler = BackgroundScheduler()

def _task_id(task):
    logging.info("scheduler_%s"%task.id)
    return "scheduler_%s"%task.id

def add_task(task):
    trigger_kwargs = json.loads(task.expr)
    _scheduler.add_job(run_case_test,args=[task.case_id],trigger="cron",id=_task_id(task),**trigger_kwargs)
    # _scheduler.add_job(run_case_task,args=[task.case_id],trigger="cron",id=_task_id(task),**trigger_kwargs)

def remove_task(task):
    job = _scheduler.get_job(_task_id(task))
    if job:
        _scheduler.remove_job(_task_id(task))

_scheduler._logger = logging

_scheduler.start()


