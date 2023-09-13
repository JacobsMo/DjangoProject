import logging
import redis
import json
from djangoproject.celery_ import app
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.template import TemplateDoesNotExist, loader
from djangoproject.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from users.repository import UserRepository
from djangoproject.settings import REDIS_HOST


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@app.task
def start_mailing(mailing_id: int, subject: str, message: str, filter: str, template_name: str):
    r = redis.Redis(host=REDIS_HOST, db=0)
    mailing_data = json.loads(r.get(str(mailing_id)))
    mailing_data["status"] = "running"

    r.set(name=str(mailing_id), value=json.dumps(mailing_data))

    users = UserRepository.get_users_without_date_joined_field()
    for user in users:
        try:
            html_document = loader.render_to_string(f"mailing/{template_name}", {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"]
            })
        except TemplateDoesNotExist:
            html_document = loader.render_to_string('mailing/mailing_template.html', {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"]
            })
            logger.info("Chose default template")

        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [user["email"]],
            fail_silently=False,
            auth_user=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            html_message=html_document
        )
        logger.info(f"Sent to: {user['email']}")
    
    mailing_data = json.loads(r.get(str(mailing_id)))
    mailing_data["status"] = "finished"
    r.set(name=str(mailing_id), value=json.dumps(mailing_data))
