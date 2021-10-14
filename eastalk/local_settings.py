from .settings import *
# PROJECT_ROOT, SITE_ROOT
import os

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    # 'default': {
    #     'ENGINE': env('DB_ENGINE'),
    #     'NAME': env('DB_NAME'),
    #     'USER': env('DB_USER'),
    #     'PASSWORD': env('DB_PASS'),
    #     'HOST': '127.0.0.1',
    #     'PORT': env('DB_PORT')
    # }
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}


