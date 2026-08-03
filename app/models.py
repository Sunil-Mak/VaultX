from datetime import datetime

from flask_login import UserMixin

from .extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    profile_image = db.Column(
        db.String(255),
        default="default-avatar.png"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
    )
    
# -------------------------------
# Document Model
# -------------------------------    
    
class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255), nullable=False)

    original_name = db.Column(db.String(255), nullable=False)

    category = db.Column(db.String(100))

    file_size = db.Column(db.Integer)

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    extracted_text = db.Column(db.Text)

    is_encrypted = db.Column(
        db.Boolean,
        default=True
    )

    ai_summary = db.Column(db.Text)

    ai_category = db.Column(db.String(100))

    ai_confidence = db.Column(db.Integer)

    ai_analysis = db.Column(db.Text)

    user = db.relationship(
        "User",
        backref="documents"
    )

   