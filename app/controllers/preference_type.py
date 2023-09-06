from sqlalchemy.orm import Session
import app.libs.database.preference_type as preference_type_db
import app.schemas.preference_type as schema_preference_type

class PreferenceTypeController:
    def get_preference_types(self, db: Session, skip: int = 0, limit: int = 1000):
        preference_types = preference_type_db.get_preference_types(db=db, skip=skip, limit=limit)
        
        return preference_types or []
    def create_preference_type(self, db: Session, preference_type=schema_preference_type.PreferenceType):
        data = preference_type_db.get_preference_type_by_id(db=db, preference_type_id=preference_type.preference_type_id)
        if data:
            return False
        
        return preference_type_db.create_preference_type(db=db, preference_type=preference_type)
    def update_preference_type(self, db: Session, preference_type_id=int, preference_type=schema_preference_type.PreferenceType):
        dataPreferenceTypeById = preference_type_db.get_preference_type_by_id(db=db, preference_type_id=preference_type_id)
        if not dataPreferenceTypeById:
            return 404
        
        return preference_type_db.update_preference_type_by_id(db=db, preference_type_id=preference_type_id, preference_type=preference_type)
    def delete_preference_type(self, db: Session, preference_type_id=int):
        dataPreferenceTypeById = preference_type_db.get_preference_type_by_id(db=db, preference_type_id=preference_type_id)
        if not dataPreferenceTypeById:
            return 404
        
        return preference_type_db.delete_preference_type_by_id(db=db, preference_type_id=preference_type_id)