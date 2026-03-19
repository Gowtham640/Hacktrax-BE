from __future__ import print_function
from celery import Celery
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = (
    f"rediss://:{os.getenv('REDIS_PASSWORD')}"
    f"@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT', 6379)}/0"
)

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.broker_use_ssl = {"ssl_cert_reqs": False}
celery_app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": False}

def send_welcome_email(to_email: str, to_name: str):
    configuration = sib_api_v3_sdk.Configuration() 
    configuration.api_key["api-key"] = os.getenv("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)    
    )

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        sender={"name": "Alexa Dev", "email": "meyyappan055@gmail.com"},
        subject="Hello There",
        html_content=f"<h2>Hi {to_name}!</h2><p>Thanks for registering!</p>"
    )

    try:
        api_response = api_instance.send_transac_email(email)
        print("Email sent:", api_response)
    except ApiException as e:
        print("Exception when sending email: %s\n" % e)
        raise e

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email_task(self, email: str, name: str):
    try:
        send_welcome_email(email, name)
    except Exception as exc:
        raise self.retry(exc=exc)