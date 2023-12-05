from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

#課題テーブル
class Task(db.Model):
    
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    
    task_title = db.Column(db.String(50),nullable=False)
    
    task_content = db.Column(db.Text)
    
    is_completed = db.Column(db.Boolean,default=False)
    
    def __str__(self):
        return f'課題ID:{self.id} タイトル:{self.task_title} 課題内容：{self.task_content} 完了フラグ:{self.is_completed}'
    
#ユーザーテーブル
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) 
    
    username = db.Column(db.String(30),unique=True,nullable=False)
    
    password = db.Column(db.String(20),nullable=False)
    
    def set_password(self,password):
        
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        
        return check_password_hash(self.password,password)
        
        