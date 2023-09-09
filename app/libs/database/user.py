from sqlalchemy.orm import Session
import app.models.user as user_model

def get_user_by_id(db: Session, user_id: int):
    results = db.query(user_model.User).filter(user_model.User.user_id == user_id).first()
    return results

def get_users(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(user_model.User).offset(skip).limit(limit).all()
    return results

def get_users_by_role(db: Session, role: int, skip: int = 0, limit: int = 1000):
    results = db.query(user_model.User).filter(user_model.User.role == role).offset(skip).limit(limit).all()
    return results

def get_users_by_two_roles(db: Session, role1: int, role2: int, skip: int = 0, limit: int = 1000):
    results = db.query(user_model.User).filter((user_model.User.role == role1) | (user_model.User.role == role2)).offset(skip).limit(limit).all()
    return results

def get_user_by_username(db: Session, username: str):
    results = db.query(user_model.User).filter(user_model.User.username == username).first()
    return results

def create_user(db: Session, user: user_model.User):
    db_user = user_model.User(
        username=user.username,
        password=user.password,
        name=user.name,
        position=user.position,
        role=user.role,
        weight=user.weight,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_id(db: Session, user_id: int, user: user_model.User):
    db_user = db.query(user_model.User).filter(user_model.User.user_id == user_id).first()
    db_user.username = user.username
    db_user.password = user.password
    db_user.name = user.name
    db_user.position = user.position
    db_user.role = user.role
    db_user.weight = user.weight
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user