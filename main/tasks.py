from post_office.mail import send_queued_mail_until_done
from django.core.management import call_command

from ecommerce.celery import app


@app.task
def mail_queue():
    send_queued_mail_until_done()
    
@app.task
def clear_sessions():
    call_command('clearsessions')