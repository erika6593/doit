import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/Users/USER/miniconda3/envs/djangoenv/lib/python3.8/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psychology_project.settings')

application = get_wsgi_application()