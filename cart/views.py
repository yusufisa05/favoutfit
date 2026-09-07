from django.shortcuts import render

# Create your views here.

import os
from pathlib import Path

# BASE_DIR: Projenin ana klasörünü otomatik bulur
BASE_DIR = Path(__file__).resolve().parent.parent

# Güvenlik Anahtarı (Geliştirme aşamasında kalabilir, yayına alırken değiştirilir)
SECRET_KEY = 'django-insecure-favoutfit-projesi-icin-gecici-anahtar'

# Hata ayıklama modu AÇIK (Hataları ekranda görebilmen için)
DEBUG = True

ALLOWED_HOSTS = []

# YÜKLÜ UYGULAMALAR (Kendi oluşturduğun app'leri buraya ekledik)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Senin uygulamaların:
    'products',
    'users',
    'cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# TEMPLATES AYARI: Django'nun senin 'templates' klasörünü bulmasını sağlar
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Ana dizindeki templates klasörü
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

WSGI_APPLICATION = 'core.wsgi.application'

# VERİTABANI: Varsayılan SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# DİL VE SAAT DİLİMİ (Türkiye için ayarlandı)
LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# İŞTE SENİN TASARIMINI (CSS) VE GÖRSELLERİNİ ÇALIŞTIRACAK KISIM
# ---------------------------------------------------------

# Statik dosyalar (CSS, JS)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Medya dosyaları (Ürün görselleri, bannerlar vs.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
