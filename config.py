'''
アプリの設定
'''

class Config(object):
    DEBUG = True
    
    SECRET_KEY = 'secret-key'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///tasks.sqlite"