import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'bb.settings'
django.setup()
from tgdelo.views import main


class Runbot():
    main()
