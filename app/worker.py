from celery import Celery
from .app import app

# в докере ругается:
# "from .app import app
# worker_1  | ImportError: attempted relative import with no known parent package"


# "from parser_app.app import app
# parser    | ModuleNotFoundError: No module named 'parser_app'"


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
