from sqlalchemy.orm import Session
import app.libs.database.user as user_db
import app.schemas.user as schema_user
import app.libs.utils.hash as hash

class UserController:
    def get_users(self, db: Session, role: int = None, skip: int = 0, limit: int = 1000):
        if role is None:
            users = user_db.get_users(db=db, skip=skip, limit=limit)
        else:
            users = user_db.get_users_by_role(db=db, role=role, skip=skip, limit=limit)
            
        return users or []
    def create_user(self, db: Session, user=schema_user.User):
        data = user_db.get_user_by_username(db=db, username=user.username)
        if data:
            return False
        
        user.password = hash.hash_password(user.password)
        
        return user_db.create_user(db=db, user=user)
    def update_user(self, db: Session, user_id=int, user=schema_user.User):
        dataUserById = user_db.get_user_by_id(db=db, user_id=user_id)
        if not dataUserById:
            return 404
        
        datauserByUsername = user_db.get_user_by_username(db=db, username=user.username)
        if datauserByUsername and datauserByUsername.user_id != user_id:
            return 409
        
        if not user.password:
            print("masuk disini")
            user.password = dataUserById.password
        else:
            user.password = hash.hash_password(user.password)
        
        return user_db.update_user_by_id(db=db, user_id=user_id, user=user)
    def delete_user(self, db: Session, user_id=int):
        dataUserById = user_db.get_user_by_id(db=db, user_id=user_id)
        if not dataUserById:
            return 404
        
        return user_db.delete_user_by_id(db=db, user_id=user_id)
    
    def login_user(self, db: Session, username=str, password=str):
        dataUserByUsername = user_db.get_user_by_username(db=db, username=username)
        if not dataUserByUsername:
            return 404
        
        if not hash.check_password(password, dataUserByUsername.password):
            return 401
        
        return dataUserByUsername