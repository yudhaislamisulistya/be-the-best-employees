from sqlalchemy.orm import Session
import app.models.batch as batch_model

def get_batch_by_code(db: Session, code: str):
    return db.query(batch_model.Batch).filter(batch_model.Batch.batch_code == code).first()

def get_batch_by_id(db: Session, batch_id: int):
    return db.query(batch_model.Batch).filter(batch_model.Batch.batch_id == batch_id).first()

def get_batchs(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(batch_model.Batch).order_by(batch_model.Batch.batch_id.asc()).offset(skip).limit(limit).all()
    return results

def create_batch(db: Session, batch: batch_model.Batch):
    db_batch = batch_model.Batch(
        batch_code=batch.batch_code,
        name=batch.name,
        description=batch.description,
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def update_batch_by_id(db: Session, batch_id: int, batch: batch_model.Batch):
    db_batch = db.query(batch_model.Batch).filter(batch_model.Batch.batch_id == batch_id).first()
    db_batch.batch_code = batch.batch_code
    db_batch.name = batch.name
    db_batch.description = batch.description
    db.commit()
    db.refresh(db_batch)
    return db_batch

def delete_batch_by_id(db: Session, batch_id: int):
    db_batch = db.query(batch_model.Batch).filter(batch_model.Batch.batch_id == batch_id).first()
    db.delete(db_batch)
    db.commit()
    return db_batch