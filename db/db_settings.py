# Database sepecific settings.
DATABASES = {
    'default': { },
    'auth_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'finder',
        'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
    'finder1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'finder',
        'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
    'finder2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'finder',
        'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
}

# temp live server fix
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'finder',
    'USER': 'finder',
    'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
    'HOST': '',
    'PORT': '',
}
DATABASES['auth_db'] = DATABASES['db1'] = DATABASES['db2'] = DATABASES['default']

# Database routers go here:
DATABASE_ROUTERS = ['my_qrcode.routers.UserRouter']
