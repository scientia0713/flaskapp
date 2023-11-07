from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#課題テーブル
class Task(db.Model):
    
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    
    task_title = db.Column(db.String(50),nullable=False)
    
    task_content = db.Column(db.Text)
    
    is_completed = db.Column(db.Boolean,default=False)
    
    def __str__(self):
        return f'課題ID:{self.id} タイトル:{self.task_title} 完了フラグ:{self.is_completed}'