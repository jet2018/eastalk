# PROJECT_ROOT, SITE_ROOT

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eastalks',
        "PASSWORD": "peacebewithyouall2020",
        "HOST": "localhost",
        "PORT": "3306",
        "USER": "root"
    }
}
