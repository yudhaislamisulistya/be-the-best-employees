from sqlalchemy.orm import Session
from fastapi import Request
import app.libs.database.ranking as ranking_db
import app.libs.database.user as user_db
import app.libs.database.employee as employee_db
import app.schemas.ranking as schema_ranking
from natsort import natsorted

class RankingController:
    def get_rankings(self, db: Session, skip: int = 0, limit: int = 1000):
        rankings = ranking_db.get_rankings(db=db, skip=skip, limit=limit)
        
        return rankings or []
    def create_ranking(self, db: Session, ranking=schema_ranking.Ranking):
        data = ranking_db.get_ranking_by_id(db=db, ranking_id=ranking.ranking_id)
        if data:
            return False
        
        return ranking_db.create_ranking(db=db, ranking=ranking)
    def update_ranking(self, db: Session, ranking_id=int, ranking=schema_ranking.Ranking):
        dataRankingById = ranking_db.get_ranking_by_id(db=db, ranking_id=ranking_id)
        if not dataRankingById:
            return 404
        
        return ranking_db.update_ranking_by_id(db=db, ranking_id=ranking_id, ranking=ranking)
    def delete_ranking(self, db: Session, ranking_id=int):
        dataRankingById = ranking_db.get_ranking_by_id(db=db, ranking_id=ranking_id)
        if not dataRankingById:
            return 404
        
        return ranking_db.delete_ranking_by_id(db=db, ranking_id=ranking_id)
    def bulk_create_ranking(self, db: Session, data: Request):
        ranking_db.bulk_create_ranking(db=db, rankings=data)
        return 200
    def bulk_create_or_update_ranking(self, db: Session, data: Request):
        ranking_db.bulk_create_or_update_ranking(db=db, rankings=data)
        return 200
    def get_ranking_by_batch_code_and_user_id(self, db: Session, batch_code: str, user_id: int):
        data = ranking_db.get_ranking_by_batch_code_and_user_id(db=db, batch_code=batch_code, user_id=user_id)
        if not data:
            return 404
        return 200
    def get_rankings_by_batch_code(self, db: Session, batch_code: str, skip: int = 0, limit: int = 1000):
        rankings = ranking_db.get_rankings_by_batch_code(db=db, batch_code=batch_code, skip=skip, limit=limit)
        return rankings or []
    def get_rankings_copeland(self, db: Session, skip: int = 0, limit: int = 1000):
        results = ranking_db.get_rankings(db=db, skip=skip, limit=limit)
        uniqueEmployeeCode = [result.employee_code for result in results]
        uniqueEmployeeCode = list(dict.fromkeys(uniqueEmployeeCode))
        uniqueEmployeeCode = natsorted(uniqueEmployeeCode)
        uniqueUserId = [result.user_id for result in results]
        uniqueUserId = list(dict.fromkeys(uniqueUserId))
        uniqueUserId = natsorted(uniqueUserId)
        uniqueUser = [user_db.get_user_by_id(db=db, user_id=userId) for userId in uniqueUserId]
        uniqueUser = [user for user in uniqueUser if user]
        results = natsorted(results, key=lambda x: x.user_id)

        pairwise_contest = []
        # tabel pairwise contest
        
        for i in range(len(uniqueEmployeeCode)):
            for j in range(len(uniqueEmployeeCode)):
                if i != j:
                    pairwise_contest.append({
                        "employee_code": uniqueEmployeeCode[i],
                        "employee_code_vs": uniqueEmployeeCode[j],
                        "user_id_win": [],
                        "user_id_lose": [],
                        "win": "",
                        "lose": "",
                        "string_score_win": "",
                        "score_win": 0,
                        "string_score_lose": "",
                        "score_lose": 0,
                    })

        for pc in pairwise_contest:
            # mencari ranking untuk employee_code dan employee_code_vs
            ranking_ec = [r.ranking for r in results if r.employee_code == pc['employee_code']]
            ranking_ec_vs = [r.ranking for r in results if r.employee_code == pc['employee_code_vs']]
            print("Ini Adalah, ", ranking_ec, " VS ", ranking_ec_vs)
            
            # len uniqueUserId
            len_uniqueUserId = len(uniqueUserId)
            # membandingkan ranking
            for i in range(len_uniqueUserId):
                if ranking_ec[i] is not None and ranking_ec_vs[i] is not None:
                    if ranking_ec[i] < ranking_ec_vs[i]:
                        print(ranking_ec[i], " < ", ranking_ec_vs[i])
                        pc['user_id_win'].append(uniqueUserId[i])
                    elif ranking_ec[i] > ranking_ec_vs[i]:
                        print(ranking_ec[i], " > ", ranking_ec_vs[i])
                        pc['user_id_lose'].append(uniqueUserId[i])
            # add win based count user_id_win
            if len(pc['user_id_win']) > len(pc['user_id_lose']):
                pc['win'] = pc['employee_code']
                pc['lose'] = pc['employee_code_vs']
                pc['string_score_win'] = [str(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_win']]
                pc['string_score_win'] = ', '.join(pc['string_score_win'])
                pc['score_win'] = [int(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_win']]
                pc['score_win'] = sum(pc['score_win'])
                pc['string_score_lose'] = [str(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_lose']]
                pc['string_score_lose'] = ', '.join(pc['string_score_lose'])
                pc['score_lose'] = [int(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_lose']]
                pc['score_lose'] = sum(pc['score_lose'])
            elif len(pc['user_id_win']) < len(pc['user_id_lose']):
                pc['win'] = pc['employee_code_vs']
                pc['lose'] = pc['employee_code']
                pc['string_score_win'] = [str(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_lose']]
                pc['string_score_win'] = ', '.join(pc['string_score_win'])
                pc['score_win'] = [int(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_lose']]
                pc['score_win'] = sum(pc['score_win'])
                pc['string_score_lose'] = [str(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_win']]
                pc['string_score_lose'] = ', '.join(pc['string_score_lose'])
                pc['score_lose'] = [int(uniqueUser[i].weight) for i in range(len_uniqueUserId) if uniqueUserId[i] in pc['user_id_win']]
                pc['score_lose'] = sum(pc['score_lose'])
                
        total_win_employee_code_to_employee_code_vs = []
        for ec1 in uniqueEmployeeCode:
            for ec2 in uniqueEmployeeCode:
                total_win_employee_code_to_employee_code_vs.append({
                    "employee_code": ec1,
                    "employee_code_vs": ec2,
                    "total_win": 0,
                    "total_lose": 0,
                })
        
        for pc in pairwise_contest:
            for i in range(len(total_win_employee_code_to_employee_code_vs)):
                if total_win_employee_code_to_employee_code_vs[i]['employee_code'] == pc['employee_code'] and total_win_employee_code_to_employee_code_vs[i]['employee_code_vs'] == pc['employee_code_vs']:
                    total_win_employee_code_to_employee_code_vs[i]['total_win'] += len(pc['user_id_win'])
                if total_win_employee_code_to_employee_code_vs[i]['employee_code'] == pc['employee_code_vs'] and total_win_employee_code_to_employee_code_vs[i]['employee_code_vs'] == pc['employee_code']:
                    total_win_employee_code_to_employee_code_vs[i]['total_lose'] += len(pc['user_id_win'])

        
        # Initialize a list to store total wins, total score, and string score for each employee
        total_win_lose_pairwise_contest = []

        for ec in uniqueEmployeeCode:
            total_win_lose_pairwise_contest.append({
                "employee_code": ec,
                "name_employee": "",
                "total_win": 0,
                "total_lose": 0,
                "difference": 0,
                "rank": 0,
            })
            
        for i in range(len(uniqueEmployeeCode)):
            total_win_lose_pairwise_contest[i]['name_employee'] = employee_db.get_employee_by_code(db=db, code=uniqueEmployeeCode[i]).name
            
        for pc in pairwise_contest:
            index = [i for i in range(len(total_win_lose_pairwise_contest)) if total_win_lose_pairwise_contest[i]['employee_code'] == pc['win']]
            total_win_lose_pairwise_contest[index[0]]['total_win'] += 1
            index = [i for i in range(len(total_win_lose_pairwise_contest)) if total_win_lose_pairwise_contest[i]['employee_code'] == pc['lose']]
            total_win_lose_pairwise_contest[index[0]]['total_lose'] += 1
            
        for i in range(len(total_win_lose_pairwise_contest)):
            total_win_lose_pairwise_contest[i]['total_win'] /= 2
            total_win_lose_pairwise_contest[i]['total_lose'] /= 2
            
        for i in range(len(total_win_lose_pairwise_contest)):
            total_win_lose_pairwise_contest[i]['difference'] = total_win_lose_pairwise_contest[i]['total_win'] - total_win_lose_pairwise_contest[i]['total_lose']
        
        # sort by total_win_lose_pairwise_contest difference
        total_win_lose_pairwise_contest = sorted(total_win_lose_pairwise_contest, key=lambda x: x['difference'], reverse=True)
        
        for i in range(len(total_win_lose_pairwise_contest)):
            total_win_lose_pairwise_contest[i]['rank'] = i + 1
        
        final_result = {
            "results": [ranking.as_dict_default_ranking() for ranking in results],
            "unique_employee_code": uniqueEmployeeCode,
            "unique_user": [user.as_dict_default_user() for user in uniqueUser],
            "pairwise_contest": pairwise_contest,
            "total_win_lose_pairwise_contest": total_win_lose_pairwise_contest,
            "total_win_employee_code_to_employee_code_vs": total_win_employee_code_to_employee_code_vs
        }
        return final_result
        