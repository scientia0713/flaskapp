'''
アプリの設定
'''

class Config(object):
    DEBUG = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///tasks.sqlite"