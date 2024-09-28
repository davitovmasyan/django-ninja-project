from project.settings import *  # noqa: F403

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'test')  # noqa: F405
USE_TZ = False
