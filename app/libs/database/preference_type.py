from sqlalchemy.orm import Session
import app.models.preference_type as preference_type_model

def get_preference_type_by_id(db: Session, preference_type_id: int):
    return db.query(preference_type_model.PreferenceType).filter(preference_type_model.PreferenceType.preference_type_id == preference_type_id).first()

def get_preference_types(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(preference_type_model.PreferenceType).order_by(preference_type_model.PreferenceType.preference_type_id.asc()).offset(skip).limit(limit).all()
    return results

def create_preference_type(db: Session, preference_type: preference_type_model.PreferenceType):
    db_preference_type = preference_type_model.PreferenceType(
        name=preference_type.name,
        type=preference_type.type,
    )
    db.add(db_preference_type)
    db.commit()
    db.refresh(db_preference_type)
    return db_preference_type

def update_preference_type_by_id(db: Session, preference_type_id: int, preference_type: preference_type_model.PreferenceType):
    db_preference_type = db.query(preference_type_model.PreferenceType).filter(preference_type_model.PreferenceType.preference_type_id == preference_type_id).first()
    db_preference_type.name = preference_type.name
    db_preference_type.type = preference_type.type
    db.commit()
    db.refresh(db_preference_type)
    return db_preference_type

def delete_preference_type_by_id(db: Session, preference_type_id: int):
    db_preference_type = db.query(preference_type_model.PreferenceType).filter(preference_type_model.PreferenceType.preference_type_id == preference_type_id).first()
    db.delete(db_preference_type)
    db.commit()
    return db_preference_type