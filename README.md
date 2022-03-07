# dev-blog

# Alhamdulillah

Akhirnya saya memutuskan untuk membagikan <em>source code</em> blog saya, namun teman-teman jangan berharap banyak dari project ini. Sebab ini hanyalah project kecil, berupa web blog biasa saja, yang membedakan hanyalah bahasa dan framework yang digunakan. Sungguh tidak ada yang istimewa di dalamnya.</p>

Front end template:
=======================================================
* Template Name: DevFolio - v2.3.0
* Template URL: https://bootstrapmade.com/devfolio-bootstrap-portfolio-html-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
========================================================

Admin templte: django-jazzmin (LTE)

# fitur

1. Blog
2. sitemap.xml dan yandex.xml
3. dioptimasi untuk SEO
4. multi user dengan group
5. sidebar (static) pencarian artikel, kategori, artikel terbaru, random related artikel
6. admin (django-jazzmin) https://github.com/farridav/django-jazzmin
7. user social login (django-allauth) caranya : https://django-allauth.readthedocs.io/en/latest/providers.html

# Lisensi 

Meski devblog yang saya hasilkan ini masih jelek, namun tetap dirasa perlu menyematkan lisensi dalam penggunaannya. Bukanlah sebuah lisensi yang aneh-aneh, project ini saya beri lisensi <strong>GNU General Public License v3.0</strong>, agar siapa saja bisa memanfaatkan project ini untuk kepentingannya masing-masing.Silahkan kalian pelajari tentang lisensi GNU V3.0. https://github.com/edikartono-com/dev-blog/blob/main/LICENSE

Namun karena project ini tidak murni 100% karya saya, maka bisa saja terdapat perbedaan lisensi diantaranya: 

Template (backend dan frontend) juga module yang digunakan. Masing-masing memiliki lisensinya sendiri.

# Cara Menggunakannya
Sebenarnya tidak sulit menggunakan devblog, 

siapkan sebuah virtual environment, buat project dan

<code>clone https://github.com/edikartono-com/dev-blog.git</code>

Buka file settings.py tambahkan
<pre><code>
import os

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',

    'ckeditor',
    'ckeditor_uploader',
    #'compressor',
    'django_seo_js',
    'imagekit',
    'taggit',
    'widget_tweaks',

    # app
    'akun',
    'corecode',
    'posts',
    # app ini masih rencana ha ha ha ...
    'products', # halaman product
    'sibmail', # next untuk email marketing (newsletter dan subscribe)
]

MIDDLEWARE = [
    'django_seo_js.middleware.EscapedFragmentMiddleware',  # If you're using #!
    'django_seo_js.middleware.UserAgentMiddleware',  # If you want to detect by user agent
    'corecode.middleware.IntroMiddleware',
    'corecode.middleware.GetSiteID',
]

TEMPLATES = [
    {
        .....

        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        ....

        'OPTIONS': {
            'context_processors': [

                .......

                'corecode.context_processors.main_menu',
                'corecode.context_processors.page_menu',

		.........

            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django login redirection
# hanya diisi dengan huruf, angka, dan tanda - tanpa spasi.
LOGIN_REDIRECT_URL = "/apa-saja-terserah/"


# django-allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# autentikasi dengan username
ACCOUNT_AUTHENTICATION_METHOD = "username"

# required email saat registrasi
ACCOUNT_EMAIL_REQUIRED = True

# registrasi tanpa verifikasi email
ACCOUNT_EMAIL_VERIFICATION = None

# batas max setelah user salah password
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

# email harus unik, satu user satu email
ACCOUNT_UNIQUE_EMAIL = True

# username yang tidak boleh digunakan
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'edikartono', 'administrator']

# minimal karakter username
ACCOUNT_USERNAME_MIN_LENGTH = 4

SITE_ID = 1

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    # config social akun untuk login lihat di: https://django-allauth.readthedocs.io/en/latest/providers.html#
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

# CKEDITOR_UPLOADER
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    'default': {
        #'skin': 'moono',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'RemoveFormat', 'Bold', 'Italic', 'Underline'],
            ['Undo', 'Redo'],
            ['NumberedList', 'BulletedList', 'Font', 'FontSize'],
            ['Blockquote', 'TextColor', 'BGColor'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'MediaEmbed', 'Smiley', 'Table', 'SpecialChar'],
            ['Source', 'toc']
        ],
        'extraPlugins': ','.join([
            'uploadimage', 'widget', 'lineutils', 'toc', 'prism', 'lazyload'
        ]), # toc prism lazyload
        'removePlugins': 'exportpdf',
        'width': '100%'
    }
}

CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_UPLOAD_PATH = 'inline-image/'

# django-htmlmin
HTML_MINIFY = True

# django-seo-js
SEO_JS_PRERENDER_TOKEN = "123456789abcdefghijkl"
SEO_JS_ENABLED = True
SEO_JS_USER_AGENTS = [
    #"Googlebot",
    #"Yahoo",
    #"bingbot",
    "Badiu",
    "Ask Jeeves",
]
SEO_JS_SEND_USER_AGENT = True
SEO_JS_IGNORE_EXTENSIONS = [
    ".xml",
    ".txt",
    # See helpers.py for full list of extensions ignored by default.
]

# MESSAGE TAG
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'
}

# django-jazzmin
# pengaturan lebih lengkap lihat di https://django-jazzmin.readthedocs.io/
JAZZMIN_SETTINGS = {
#     "site_title": "Edi Kartono",
#     "site_header": "I am EDI KARTONO",
    "site_logo": "img/logo.png",
    "site_icon": "img/logo.png",
}
</code></pre>

isntall module python yang dibutuhkan   

<pre><code>pip install -r requirements.txt

python manage.py migrate

python manage.py runserver</code></pre>

# masih ada error
Beberapa masih belum sempurna, seperti yandex.xml yang belum bisa diakses.

# to do
1. email marketing (subscribe dan newsletter)
2. dashboard user
3. Product dan shopping cart