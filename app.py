import os
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Task(db.Model):
    
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    
    content = db.Column(db.String(200),nullable=False)
    
    is_completed = db.Column(db.Boolean,default=False)
    
    def __str__(self):
        return f'課題ID:{self.id} 内容:{self.content} 完了フラグ:{self.is_completed}'

#一覧
@app.route('/')
def index():
    #未完了課題一覧
    uncompleted_tasks = Task.query.filter_by(is_completed=False).all()
    
    #完了課題一覧
    completed_tasks = Task.query.filter_by(is_completed=True).all()
    
    return render_template('index.html',uncompleted_tasks=uncompleted_tasks,completed_tasks=completed_tasks)

#登録
@app.route('/new',methods=['GET','POST'])
def new_task():
    #POSTの場合
    if request.method == 'POST':
        content = request.form['content']
        
        task = Task(content=content)
        
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    #GETの場合
    return render_template('new_task.html')

#完了ボタン押下時
@app.route('/tasks/<int:task_id>/complete',methods=['POST'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.is_completed = True
    db.session.commit()
    return redirect(url_for('index'))

#未完了ボタン押下時
@app.route('/tasks/<int:task_id>/uncomplete',methods=['POST'])
def uncomplete_task(task_id):
    task = Task.query.get(task_id)
    task.is_completed = False
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
