from .base import *
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
# ROOT_URLCONF = 'portfolioLedger.urls'
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')

