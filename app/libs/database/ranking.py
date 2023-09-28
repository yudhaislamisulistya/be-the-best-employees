from sqlalchemy.orm import Session
import app.models.ranking as ranking_model
from sqlalchemy.dialects.postgresql import insert

def get_ranking_by_id(db: Session, ranking_id: int):
    return db.query(ranking_model.Ranking).filter(ranking_model.Ranking.ranking_id == ranking_id).first()

def get_rankings(db: Session, skip: int = 0, limit: int = 1000):
    results = db.query(ranking_model.Ranking).order_by(ranking_model.Ranking.ranking_id.asc()).offset(skip).limit(limit).all()
    return results

def create_ranking(db: Session, ranking: ranking_model.Ranking):
    db_ranking = ranking_model.Ranking(
        user_id = ranking.user_id,
        batch_code = ranking.batch_code,
        employee_code = ranking.employee_code,
        name = ranking.name,
        net_flow = ranking.net_flow,
        ranking = ranking.ranking
    )
    db.add(db_ranking)
    db.commit()
    db.refresh(db_ranking)
    return db_ranking

def bulk_create_ranking(db: Session, rankings: list):
    db.execute(ranking_model.Ranking.__table__.insert(), rankings)
    db.commit()
    return rankings

def bulk_create_or_update_ranking(db: Session, rankings: list):
    upsert_stmt = insert(ranking_model.Ranking).values(rankings)
    upsert_stmt = upsert_stmt.on_conflict_do_update(
        index_elements=[ranking_model.Ranking.ranking_id],
        set_={
            "user_id": upsert_stmt.excluded.user_id,
            "batch_code": upsert_stmt.excluded.batch_code,
            "employee_code": upsert_stmt.excluded.employee_code,
            "name": upsert_stmt.excluded.name,
            "net_flow": upsert_stmt.excluded.net_flow,
            "ranking": upsert_stmt.excluded.ranking
        }
    )

def update_ranking_by_id(db: Session, ranking_id: int, ranking: ranking_model.Ranking):
    db_ranking = db.query(ranking_model.Ranking).filter(ranking_model.Ranking.ranking_id == ranking_id).first()
    db_ranking.user_id = ranking.user_id
    db_ranking.batch_code = ranking.batch_code
    db_ranking.employee_code = ranking.employee_code
    db_ranking.name = ranking.name
    db_ranking.net_flow = ranking.net_flow
    db_ranking.ranking = ranking.ranking
    db.commit()
    db.refresh(db_ranking)
    return db_ranking

def delete_ranking_by_id(db: Session, ranking_id: int):
    db_ranking = db.query(ranking_model.Ranking).filter(ranking_model.Ranking.ranking_id == ranking_id).first()
    db.delete(db_ranking)
    db.commit()
    return db_ranking

def get_ranking_by_batch_code_and_user_id(db: Session, batch_code: str, user_id: int):
    return db.query(ranking_model.Ranking).filter(ranking_model.Ranking.batch_code == batch_code, ranking_model.Ranking.user_id == user_id).first()

def get_rankings_by_batch_code(db: Session, batch_code: str, skip: int = 0, limit: int = 1000):
    results = db.query(ranking_model.Ranking).filter(ranking_model.Ranking.batch_code == batch_code).order_by(ranking_model.Ranking.ranking_id.asc()).offset(skip).limit(limit).all()
    return results