import logging
import os
from typing import List

import dj_database_url
import sentry_sdk
from django.conf import global_settings
from sentry_sdk.integrations.django import DjangoIntegration

from core.patches import patch_django

patch_django()

logger = logging.getLogger(__name__)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.getenv("DEBUG") == "1"
CI = os.getenv("CI", False)
PRODUCTION = not DEBUG and not CI
DOCKERBUILD = os.getenv("DOCKERBUILD", False)
TESTING = os.getenv("TESTING") is not None

logger.info(
    "CI:", CI, "DEBUG:", DEBUG, "PRODUCTION:", PRODUCTION, "DOCKERBUILD", DOCKERBUILD
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG or DOCKERBUILD:
    SECRET_KEY = "+p(5+wb+(l2$@iv!1*3=5xnrw2gvi+l$kuo9s7=u6*)ri4v6as"
else:
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS: List[str] = [".recipeyak.com"]

if DEBUG:
    ALLOWED_HOSTS = ["*"]

# Replaced with Git SHA during docker build. We use this to track releases via Sentry
GIT_SHA = "<%=GIT_SHA=%>"

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "user_sessions",
    "core.apps.CoreConfig",
    "rest_framework",
    "django.contrib.sites",
    "django.contrib.postgres",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

sentry_sdk.init(
    integrations=[DjangoIntegration()],
    release=GIT_SHA,
    send_default_pii=True,
    traces_sample_rate=1.0,
)

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("core.auth.permissions.DisallowAny",),
    "DEFAULT_RENDERER_CLASSES": ("core.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("core.authentication.SessionAuthentication",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Ensure request.is_secure returns true with the correct header since we're
# running behind a proxy
# see: https://docs.djangoproject.com/en/2.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://stackoverflow.com/questions/25468676/django-sites-model-what-is-and-why-is-site-id-1#25468782
SITE_ID = 1

# Required for using email and on username. http://django-allauth.readthedocs.io/en/latest/advanced.html
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"  # (="username" | "email" | "username_email)
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SESSION_COOKIE_AGE = 365 * 24 * 60 * 60  # sessions expire in one year

if not DEBUG:
    # make the cookie HTTPS only
    # https://docs.djangoproject.com/en/2.2/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True

# http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html#basic
# Require the old password be provided to change a your password
OLD_PASSWORD_FIELD_ENABLED = True

MIDDLEWARE = [
    "core.middleware.HealthCheckMiddleware",
    "core.middleware.CurrentRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.XForwardedForMiddleware",
    "core.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "core.middleware.NoCacheMiddleware",
    "core.middleware.ExceptionMiddleware",
]


SESSION_ENGINE = "user_sessions.backends.db"

if DEBUG and not TESTING:
    MIDDLEWARE += (
        "core.middleware.ServerTimingMiddleware",
        "core.middleware.APIDelayMiddleware",
    )

API_DELAY_MS = 200

AUTH_USER_MODEL = "core.User"

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"


if DEBUG or DOCKERBUILD:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {}

DATABASES["default"] = dj_database_url.config(conn_max_age=600)

ERROR_ON_SERIALIZER_DB_ACCESS = DEBUG or TESTING


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}
]

# use fast password hasher for testing
if DEBUG:
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",
        *global_settings.PASSWORD_HASHERS,
    ]

# system check framework
SILENCED_SYSTEM_CHECKS = [
    # We don't use messages and sessions in our user facing app. The admin page works fine without these too.
    # (admin.E406) 'django.contrib.messages' must be in INSTALLED_APPS in order to use the admin application.
    "admin.E406",
    # (admin.E407) 'django.contrib.sessions' must be in INSTALLED_APPS in order to use the admin application.
    "admin.E407",
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/var/app/static"

# https://docs.djangoproject.com/en/dev/topics/logging/#module-django.utils.log
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": 'level=%(levelname)s msg="%(message)s" user_id=%(user_id)s request_id=%(request_id)s name=%(name)s '
            'pathname="%(pathname)s" lineno=%(lineno)s funcname=%(funcName)s '
            "process=%(process)d thread=%(thread)d "
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["no_testing", "request_id", "user_id"],
        }
    },
    "filters": {
        "no_testing": {"()": "core.logging.TestingDisableFilter"},
        "request_id": {"()": "core.logging.RequestIDFilter"},
        "user_id": {"()": "core.logging.CurrentUserFilter"},
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["console"]},
        "django.utils.autoreload": {"propagate": False},
    },
}
