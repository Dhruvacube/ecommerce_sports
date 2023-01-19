import configparser
import os
import secrets
from pathlib import Path
from typing import Any


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return "..."

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


MISSING: Any = _MissingSentinel()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / ".conf"

def token_get(tokenname: str = MISSING, value_not_found: str = MISSING, all: bool = False) -> Any:
    """Helper function to get the credentials from the environment variables or from the configuration file
    :param tokenname: The token name to access
    :type tokenname: str
    :param all: Return all values from config filename, defaults to False
    :type all: bool, optional
    :raises RuntimeError: When all set :bool:`True` and `.ini` file is not found
    :return: The environment variables data requested if not found then None is returned
    :rtype: Any
    """
    if not all:
        if CONFIG_FILE.is_file():
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            sections = config._sections
            for i in sections:
                for j in sections[i]:
                    if j.lower() == tokenname.lower():
                        return sections[i][j]
            return value_not_found
        return os.environ.get(tokenname, "False").strip("\n")
    if CONFIG_FILE.is_file():
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config._sections
    raise RuntimeError("Could not find .ini file")

class _envConfig:
    """A class which contains all token configuration"""

    def __init__(self):
        self.data: dict = token_get(all=True)
        for i in self.data:
            for j in self.data.get(i, MISSING):
                setattr(self, j.lower().strip("\n"), self.data[i].get(j))
                setattr(self, j.upper().strip("\n"), self.data[i].get(j))


envConfig: Any = _envConfig()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = token_get('SECRET_KEY', secrets.token_urlsafe(25))

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.humanize",
    'django.contrib.postgres',
    "django_admin_listfilter_dropdown",
    "compressor"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if bool(int(token_get('POSTGRES'))) or not bool(int(token_get('SQLITE'))) and token_get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(default=token_get("DATABASE_URL"))
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

CELERY_TIMEZONE = TIME_ZONE = 'Asia/Kolkata'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR/ "static"
MEDIA_ROOT = BASE_DIR/ "media"
MEDIA_URL = "/media/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION":
        token_get("REDIS_URL", "redis://127.0.0.1:6379"),  # expected port, otherwise you can alter it
    }
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ("text/x-sass", "django_libsass.SassCompiler"),
    ("text/x-scss", "django_libsass.SassCompiler"),
)
COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.JSMinFilter",
    ],
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False

SESSION_COOKIE_AGE = 1 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = token_get("REDIS_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = token_get("CLOUDAMQP_URL", "amqp://localhost")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

DEBUG = bool(int(getattr(envConfig, 'DEBUG', 0))) 
    
if bool(int(getattr(envConfig, 'WHITENOISE', 0))):
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    MIDDLEWARE = ([MIDDLEWARE[0]] + ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE[1:])
    INSTALLED_APPS = (INSTALLED_APPS[0:-1] + ["whitenoise.runserver_nostatic"] + [INSTALLED_APPS[-1]])
    WHITENOISE_MAX_AGE = 9000
    WHITENOISE_SKIP_COMPRESS_EXTENSIONS = []



if bool(int(getattr(envConfig, 'PRODUCTION_SERVER', 0))):
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
else:
    CACHE_MIDDLEWARE_SECONDS = 0
    
if bool(int(getattr(envConfig, 'LOGGING', 0))):
    from .django_logging import LOGGING