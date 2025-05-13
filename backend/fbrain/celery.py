from __future__ import absolute_import
import os
from celery import Celery

# Nom du projet Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbrain.settings')

app = Celery('fbrain')

# Utilise les paramètres de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-détection des tâches dans les apps installées
app.autodiscover_tasks()

