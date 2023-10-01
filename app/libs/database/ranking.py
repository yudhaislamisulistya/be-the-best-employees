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

def bulk_update_ranking(db: Session, rankings: list):
    for ranking in rankings:
        print(ranking["batch_code"])
        print(ranking["user_id"])
        print(ranking["employee_code"])
        db_ranking = db.query(ranking_model.Ranking).filter(
            ranking_model.Ranking.batch_code == ranking["batch_code"], 
            ranking_model.Ranking.user_id == ranking["user_id"], 
            ranking_model.Ranking.employee_code == ranking["employee_code"]
        ).first()
        
        if db_ranking is None:
            print(f"No matching row found for batch_code={ranking['batch_code']}, user_id={ranking['user_id']}, employee_code={ranking['employee_code']}")
            continue

        db_ranking.net_flow = ranking["net_flow"]
        db_ranking.ranking = ranking["ranking"]
        db.commit()
        db.refresh(db_ranking)
    return rankings


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