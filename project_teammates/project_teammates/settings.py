"""
Django settings for project_teammates project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&6r8i_e#)^9q2+7bkfutvs$dbs$k8-kk8ln!vzc%+d$q&a^qpe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'project_teammates.apps.TeammatesConfig',
    'teammates',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'corsheaders',

    'allauth',
    'allauth.account',
    'allauth.socialaccount'#for making dependencies sorted

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_teammates.urls'

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

WSGI_APPLICATION = 'project_teammates.wsgi.application'

AUTH_USER_MODEL = 'teammates.Student'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# import psycopg2

# [START db_setup]
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': '/cloudsql/project-teammates-236620:us-central1:project-teammates',
            'USER': 'vibhu',
            'PASSWORD': 'vibhu123',
            'NAME': 'teammates',
        }
    }
else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'NAME': 'teammates',
            'USER': 'vibhu',
            'PASSWORD': 'vibhu123',
        }
    }
# [END db_setup]


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_ROOT = 'static'
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',#Allow this to allow custom authentication permission for some APIs
        # 'rest_framework.permissions.IsAuthenticated',
    ]

}

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`

    'django.contrib.auth.backends.ModelBackend',


    # `allauth` specific authentication methods, such as login by e-mail

    'allauth.account.auth_backends.AuthenticationBackend',

)

ACCOUNT_ADAPTER = "teammates.EmailValidationAccountAdapter.MyCoolAdapter"

REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': "teammates.StudentRegistrationSerializer.StudentSerializerOveride"

}

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'teammates.CustomTokenSerializer.MyTokenSerializer',
}

#----------------Settings for running on localhost------------#
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']

#----------------Settings for running on Production Google Cloud------------#
# CORS_ORIGIN_ALLOW_ALL = False
# SESSION_COOKIE_SAMESITE = None
# # SESSION_COOKIE_HTTPONLY = False
# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = 'eighth-alchemy-236004.appspot.com',
# SESSION_COOKIE_DOMAIN = '.appspot.com'
# CSRF_COOKIE_DOMAIN = '.appspot.com'
# ALLOWED_HOSTS = ['.appspot.com', "eighth-alchemy-236004.appspot.com", "localhost",]



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
    'access-control-allow-credentials',
    'Access-Control-Allow-Origin',
)


ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "projectteammatesauthentication@gmail.com"
EMAIL_HOST_PASSWORD = "01project"