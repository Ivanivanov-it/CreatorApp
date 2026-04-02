import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CreatorApp.settings.local')

app = Celery('CreatorApp',
             broker=os.getenv('CELERY_BROKER_URL'),
             backend=os.getenv('CELERY_BROKER_URL'),
                broker_use_ssl={'ssl_cert_reqs': None},
                redis_backend_use_ssl={'ssl_cert_reqs': None}
             )
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')