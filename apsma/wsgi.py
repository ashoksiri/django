"""
WSGI config for apsma project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site


from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/home/administrator/prod_bak/prodbak_env/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(BASE_DIR)

# Activate your virtual env
#activate_env=os.path.expanduser("/home/administrator/prod_bak/prodbak_env/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apsma.settings")

application = get_wsgi_application()
