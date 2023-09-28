from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class Ranking(Base):
    __tablename__ = "rankings"
    ranking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    batch_code = Column(String)
    employee_code = Column(String)
    name = Column(String)
    net_flow = Column(Float)
    ranking = Column(Integer)
    
    def __init__(self, ranking_id = None, user_id = None, batch_code = None, employee_code = None, name = None, net_flow = None, ranking = None):
        self.ranking_id = ranking_id
        self.user_id = user_id
        self.batch_code = batch_code
        self.employee_code = employee_code
        self.name = name
        self.net_flow = net_flow
        self.ranking = ranking
        
    def as_dict_default_ranking(self):
        return {
            "ranking_id": self.ranking_id,
            "user_id": self.user_id,
            "batch_code": self.batch_code,
            "employee_code": self.employee_code,
            "name": self.name,
            "net_flow": self.net_flow,
            "ranking": self.ranking
        }