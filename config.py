'''
アプリの設定
'''

class Config(object):
    DEBUG = True
    
    SQLALCHEMY_TRACK_MODIFICATION = False
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite"