from flask import render_template,request,redirect,url_for
from app import app
from models import db, Task

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
        task_title = request.form['task_title']
        
        task = Task(task_title=task_title)
        
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