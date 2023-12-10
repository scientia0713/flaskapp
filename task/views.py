'''
課題の一覧表示、CRUD管理
'''
from flask import Blueprint,render_template,request,redirect,url_for,flash
from models import db, Task,User
from forms import TaskForm,LoginForm,SignUpForm
from flask_login import login_user,logout_user,login_required

#課題管理機能のBlueprint
task_bp = Blueprint('task',__name__,url_prefix='/task')
    
#一覧
@task_bp.route('/')
@login_required
def index():
    #未完了課題一覧
    uncompleted_tasks = Task.query.filter_by(is_completed=False).all()
    
    #完了課題一覧
    completed_tasks = Task.query.filter_by(is_completed=True).all()
    
    #一覧画面に遷移
    return render_template('task/index.html',uncompleted_tasks=uncompleted_tasks,completed_tasks=completed_tasks)

#登録
@task_bp.route('/new',methods=['GET','POST'])
@login_required
def new_task():
    #POSTの場合
    form = TaskForm()
    
    #バリデーションチェック
    if form.validate_on_submit():
        #新規登録課題のタイトルを取り出す
        task_title = form.task_title.data
        
        #新規登録課題の内容を取り出す
        task_content = form.task_content.data

        #登録処理
        task = Task(task_title=task_title,task_content=task_content)
        
        db.session.add(task)
        db.session.commit()
        
        #フラッシュメッセージ
        flash('課題を1件登録しました。')
        
        #一覧画面にリダイレクト
        return redirect(url_for('task.index'))
    
    #GETの場合
    return render_template('task/new_task_form.html',form=form)

#編集
@task_bp.route('/<int:task_id>/update',methods=['GET','POST'])
@login_required
def update_task(task_id):
    target_task = Task.query.get(task_id)
    
    form = TaskForm(obj=target_task)
    
    #POST時
    #バリデーションチェック
    if request.method == 'POST' and form.validate():
        #更新処理
        target_task.task_title = form.task_title.data
        
        target_task.task_content = form.task_content.data
        
        db.session.commit()
        
        #フラッシュメッセージ
        flash('課題を1件更新しました。')
        
        #一覧画面にリダイレクト
        return redirect(url_for('task.index'))
    
    #GET時
    return render_template('task/update_task_form.html',form=form,task=target_task)

#削除
@task_bp.route('/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    target_task = Task.query.get(task_id)
    
    #削除処理
    db.session.delete(target_task)
    db.session.commit()
    
    flash('課題を1件削除しました。')
    
    #一覧画面にリダイレクト
    return redirect(url_for('task.index'))

#完了ボタン押下時
@task_bp.route('/<int:task_id>/complete',methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.is_completed = True
    db.session.commit()
    return redirect(url_for('task.index'))

#未完了ボタン押下時
@task_bp.route('/<int:task_id>/uncomplete',methods=['POST'])
@login_required
def uncomplete_task(task_id):
    task = Task.query.get(task_id)
    task.is_completed = False
    db.session.commit()
    return redirect(url_for('task.index'))