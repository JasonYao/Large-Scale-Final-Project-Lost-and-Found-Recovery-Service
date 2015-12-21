# Database sepecific settings.
DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'db1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'db2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

# Database routers go here:
DATABASE_ROUTERS = ['my_qrcode.routers.UserRouter']
