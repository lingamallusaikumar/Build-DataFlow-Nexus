from app.extensions import db
from app.auth.models import User
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    @staticmethod
    def register_user(data):
        if User.query.filter_by(email=data.email).first():
            return None, "User already exists."
        
        new_user = User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name
        )
        new_user.set_password(data.password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, None

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return {
                "access_token": create_access_token(identity=user.id),
                "refresh_token": create_refresh_token(identity=user.id)
            }, None
        return None, "Invalid email or password"
