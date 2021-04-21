"""
Django settings for andreai project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from andreai.loader import load_credential
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTING_DEV_DIC = load_credential("develop")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SETTING_DEV_DIC['SECRET_KEY']
DEBUG = True

ALLOWED_HOSTS = ['3.36.156.224', '.ap-northeast-2.compute.amazonaws.com', 'www.andre-ai.com', 'andre-ai.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'pictures',
    'landing',
    'storages',
    'corsheaders',
    'custom_manage',
    'crispy_forms',
    # 'static' ##
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'andreai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['landing/templates'],
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

WSGI_APPLICATION = 'andreai.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Default user model
AUTH_USER_MODEL = 'accounts.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

DATABASES = {
    'default': SETTING_DEV_DIC["dev"],
}
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'djangobower.finders.BowerFinder',
]
# # AWS
AWS_ACCESS_KEY_ID = SETTING_DEV_DIC['S3']['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SETTING_DEV_DIC['S3']['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = SETTING_DEV_DIC['S3']['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = SETTING_DEV_DIC['S3']['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = SETTING_DEV_DIC['S3']['AWS_S3_SIGNATURE_VERSION']
AWS_STORAGE_BUCKET_NAME = SETTING_DEV_DIC['S3']['AWS_STORAGE_BUCKET_NAME']

# AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_S3_REGION_NAME

AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)
# STATIC_LOCATION = 'static'


STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # collectstatic 할때 보는 폴더
STATIC_ROOT = os.path.join(BASE_DIR, 'static') # 배포해서는 이걸참고하기 때문에 static으로 바꾸고 위의라인을 주석처리
STATICFILES_STORAGE = 'andreai.storage.S3StaticStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'andreai.storage.S3MediaStorage'

#
# # boto only
# AWS_HEADERS = {
#     'Content-Disposition': 'attachment'
# }

# boto3 only
# AWS_S3_OBJECT_PARAMETERS = {
#     'Content-Disposition': 'attachment'
# }
#


# CORS
# CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://andre-ai.com',
    'http://www.andre-ai.com',
    'http://3.36.156.224',
    'http://localhost'
]
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)