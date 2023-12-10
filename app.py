from flask import Flask
from flask_migrate import Migrate
from models import db,User
from flask_login import LoginManager
from auth.views import auth_bp
from task.views import task_bp

app = Flask(__name__)

#設定ファイル読込
app.config.from_object("config.Config")

db.init_app(app)

migrate = Migrate(app,db)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_message = 'ログインされていません。ログイン画面よりログインしてください。'

login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

@login_manager.user_loader
def load_user(user_id):
    
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run()
