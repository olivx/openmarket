from django.utils.crypto import get_random_string

""" create .env file"""
print("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
print('create a initial .env file ')
print("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
print('')
print('')
print('')
print('')
print('')
_keys = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
_CONF_FILE = '''


SECRET_KEY={}
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .localhost
DATABASE_URL="postgis://postgres:postgres@db:5432/app"
DEBUG=True
LOG_LEVEL="INFO"
WORKERS=1
LOG_APP_FILE_STREAM=log/app.log
LOG_GUNICORN_FILE_STREAM=log/gunicorn.log



'''.format(get_random_string(50, _keys))

with open('.env', 'w') as conf:
    conf.write(_CONF_FILE)

print("***********************************************************")
print('conf file was created with  ')
print("***********************************************************")
print(_CONF_FILE)
print("-----------------------------------------------------------")
