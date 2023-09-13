import redis
import logging
import json
import ast
from random import randint
from djangoproject.settings import REDIS_HOST
from datetime import datetime
from djangoproject.celery_ import app


logger = logging.getLogger("info")


class MailingService:
    @staticmethod
    def generate_task_id() -> int:
        r = redis.Redis(host=REDIS_HOST, db=0)
        while True:
            task_id = randint(1, 999999)
            task = r.get(str(task_id))

            if task is None:
                return task_id

    @staticmethod
    def add_mailing(mailing_id: int, start_time: datetime, subject: str, message: str, filter: str) -> bool:
        mailing_data = {
            "start_time": str(start_time),
            "subject": subject,
            "message": message,
            "filter": filter,
            "status": "pending"
        }
        r = redis.Redis(host=REDIS_HOST, db=0)
        
        return r.set(name=str(mailing_id), value=json.dumps(mailing_data))

    @staticmethod
    def get_mailing_by_id(mailing_id: int) -> dict or None:
        r = redis.Redis(host=REDIS_HOST, db=0)
        mailing = r.get(name=str(mailing_id))
        return mailing if mailing is not None else None
        
    @staticmethod
    def delete_mailing_by_id(mailing_id: int) -> bool:
        r = redis.Redis(host=REDIS_HOST, db=0)
        mailing = json.loads(r.get(str(mailing_id)))

        if mailing.get("status") == "running":
            return False 

        app.control.revoke(str(mailing_id))
        return r.delete(str(mailing_id))

    @staticmethod
    def update_mailing_by_id(mailing_id: int, data: dict) -> bool:
        r = redis.Redis(host=REDIS_HOST, db=0)
        mailing_data = json.loads(r.get(str(mailing_id)))

        fields_for_update = ast.literal_eval(data["data"])

        for field in fields_for_update:
            if field in mailing_data:
                mailing_data[field] = fields_for_update[field]

        if mailing_data["status"] == "running":
            return False

        r.set(name=str(mailing_id), value=json.dumps(mailing_data))
        
        return True
