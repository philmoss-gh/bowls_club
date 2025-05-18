"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
sys.path.append('/home/your-username/bowls_club')

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Activate the virtual environment
activate_this = '/home/your-username/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
