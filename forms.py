from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,ValidationError
from models import Task

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
    