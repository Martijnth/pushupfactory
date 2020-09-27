
import os.path
import sys

sys.path.insert(0, os.path.dirname(__file__))

activate_this = os.path.abspath(os.path.join(__file__, '..', '..', 'virtual', 'bin', 'activate_this.py'))
exec(open(activate_this).read(), dict(__file__=activate_this))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
# assert not __debug__  # Make sure the server is configured for not running in debug mode. Just enable optimization to set __debug__ to false.

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
