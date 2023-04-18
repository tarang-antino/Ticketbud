from __future__ import absolute_import, unicode_literals
from .email import *
from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)


# @shared_task
# def add(x,y):
#     return x+y
# @task(name="send_email")
@shared_task()
def send_email(**data):
    print("+++++++++++++++++++++++++++++++++++")
    logger.info("Sent Email")
    # print(data)
    # return 0
    return send_review_email(data["email"], data["types"], data["info"])
    # if data["types"]=="OTP":
    #     print("+++++++++++++++++++++++++++++++++++")
    #     logger.info("Sent Email")
    #     # print(data)
    #     # return 0
    #     return send_review_email(data["email"],data["types"],data["info"])
    # elif data["types"]=="register":
    #     print("-------------------------------")
    #     logger.info("Sent Email")
    #     print(data)
    #     # return 0
    #     return send_review_email(data["email"],data["types"],data["info"])
    # elif data["types"]=="bookevent":
    #     print("-------------------------------")
    #     logger.info("Sent Email")
    #     print(data)
    #     # return 0
    #     return send_review_email(data["email"],data["types"],data["info"])
    # elif data["types"]=="updtpass":
    #     print("-------------------------------")
    #     logger.info("Sent Email")
    #     print(data)
    #     # return 0
    #     return send_review_email(data["email"],data["types"],data["info"])
