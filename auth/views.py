'''
ログイン、サインアップ、ログアウト管理
'''
from flask import Blueprint,render_template,redirect,url_for,flash
from models import db,User
from forms import LoginForm,SignUpForm
from flask_login import login_user,logout_user,login_required

#認証機能のBlueprint
auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

#ログイン
@auth_bp.route('/',methods=['GET','POST'])
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
            return redirect(url_for('task.index'))
        
        #認証失敗
        flash('ユーザー名もしくはパスワードが違います。')
    
    #GET時
    return render_template('auth/login_form.html',form=form)

#ログアウト
@auth_bp.route('/logout')
@login_required
def logout():
    
    logout_user()
    
    flash('ログアウトしました。')
    
    #ログイン画面に遷移
    return redirect(url_for('auth.login'))

#サインアップ
@auth_bp.route('/register',methods=['GET','POST'])
@login_required
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
        
        return redirect(url_for('auth.login'))
    
    #GET時
    return render_template('auth/register_form.html',form=form)
    