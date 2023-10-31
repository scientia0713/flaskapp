from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#課題テーブル
class Task(db.Model):
    
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    
    content = db.Column(db.String(400),nullable=False)
    
    is_completed = db.Column(db.Boolean,default=False)
    
    def __str__(self):
        return f'課題ID:{self.id} 内容:{self.content} 完了フラグ:{self.is_completed}'