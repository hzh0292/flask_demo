SECRET_KEY = "94853e5a-db7b-4e4f-b6c0-7e24f1beb261"
DEBUG = True
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlktqa'
USERNAME = 'root'
PASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATION = False