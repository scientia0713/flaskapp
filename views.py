from flask import render_template,request,redirect,url_for,flash
from app import app
from models import db, Task,User
from forms import TaskForm,LoginForm,SignUpForm
from flask_login import login_user,logout_user

#ログイン
@app.route('/',methods=['GET','POST'])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        
        #入力されたユーザー情報を取り出す
        username = form.username.data
        password = form.password.data
        
        #ユーザーテーブルからユーザー情報を抽出
        user = User.query.filter_by(username=username).first()
        
        #認証判定
        if user is not None and user.check_password(password):
            
            #成功　ログイン状態にする
            login_user(user)
            
            #一覧画面に遷移
            return redirect(url_for('index'))
        
        #認証失敗
        flash('ユーザー名もしくはパスワードが違います。')
    
    #GET時
    return render_template('login_form.html',form=form)

#ログアウト
@app.route('/logout')
def logout():
    
    logout_user()
    
    flash('ログアウトしました。')
    
    #ログイン画面に遷移
    return redirect(url_for('login'))

#サインアップ
@app.route('/register',methods=['GET','POST'])
def register():
    
    form = SignUpForm()
    
    if form.validate_on_submit():
        
        #登録したいユーザー情報を取り出す
        username = form.username.data
        password = form.password.data
        
        #DB登録情報生成
        user = User(username=username)
        user.set_password(password)
        
        #DB登録
        db.session.add(user)
        db.session.commit()
        
        flash('ユーザー情報を1件登録しました。')
        
        return redirect(url_for('login'))
    
    #GET時
    return render_template('register_form.html',form=form)
    
#一覧
@app.route('/tasks/')
def index():
    #未完了課題一覧
    uncompleted_tasks = Task.query.filter_by(is_completed=False).all()
    
    #完了課題一覧
    completed_tasks = Task.query.filter_by(is_completed=True).all()
    
    #一覧画面に遷移
    return render_template('index.html',uncompleted_tasks=uncompleted_tasks,completed_tasks=completed_tasks)

#登録
@app.route('/tasks/new',methods=['GET','POST'])
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
        return redirect(url_for('index'))
    
    #GETの場合
    return render_template('new_task_form.html',form=form)

#編集
@app.route('/tasks/<int:task_id>/update',methods=['GET','POST'])
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
        return redirect(url_for('index'))
    
    #GET時
    return render_template('update_task_form.html',form=form,task=target_task)

#削除
@app.route('/tasks/<int:task_id>/delete')
def delete_task(task_id):
    target_task = Task.query.get(task_id)
    
    #削除処理
    db.session.delete(target_task)
    db.session.commit()
    
    flash('課題を1件削除しました。')
    
    #一覧画面にリダイレクト
    return redirect(url_for('index'))

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