from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,ValidationError
from models import Task,User

#新規課題登録用フォーム
class TaskForm(FlaskForm):
    task_title = StringField('課題タイトル:',validators=[DataRequired('課題タイトルは必須入力です。'),
                                                   Length(max=30,message='課題タイトルは30文字以下で入力してください。')])
    task_content = TextAreaField('内容:',validators=[DataRequired('内容は必須入力です')])
    
    #登録ボタン
    submit = SubmitField('登録')
    
    #更新ボタン
    update = SubmitField('更新')
    
    def validate_task_title(self,task_title):
        task = Task.query.filter_by(task_title=task_title.data).first()
        
        if task:
            raise ValidationError(f"課題タイトル'{task_title.data}'は既に登録されています。別の課題タイトルを入力してください。")

#ログイン用フォーム     
class LoginForm(FlaskForm):
    username = StringField('ユーザー名',validators=[DataRequired('ユーザー名は必須入力です。')])
    
    password = PasswordField('パスワード',validators=[Length(8,20,'パスワードは8文字以上、20文字以内です。')])
    
    submit = SubmitField('ログイン')
    
#サインアップ用フォーム
class SignUpForm(LoginForm):
    
    submit = SubmitField('ユーザー登録')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        
        if user:
            raise ValidationError('そのユーザー名は既に使用されています。別のユーザー名で登録してください。')
    
    