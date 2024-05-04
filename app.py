from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()  # Initialize Bcrypt without app

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ADMin1234!@172.17.0.3/flask_login'
    app.config['SECRET_KEY'] = 'justasecretkeythatishouldputhere'
    
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)  # Add this line to bind Bcrypt with your app

    @login_manager.user_loader
    def load_user(user_id):
        from classes.class_user import User  # Move the import statement here
        return User.query.get(int(user_id))

    from routes.user_login_bp import user_login_bp
    app.register_blueprint(user_login_bp, url_prefix='/')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
