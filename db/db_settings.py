# Database sepecific settings.
DATABASES = {
    'default': { },
    'auth_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'finder',
        'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
        'HOST': '',
        'PORT': '',
    },
    'finder1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'finder',
        'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
        'HOST': '',
        'PORT': '',
    },
    'finder2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finder',
        'USER': 'finder',
        'PASSWORD': 'Paz*1C40!3h@SB4dxg2tR%R2n5EnriLgBZgMpAjdpOdoKum#8M4UgLFjQ%h39oRXUur6nQt6v4aEPyA$E%9aqArsYOfe4IM@H49M',
        'HOST': '',
        'PORT': '',
    },
}

# Database routers go here:
DATABASE_ROUTERS = ['my_qrcode.routers.UserRouter']
