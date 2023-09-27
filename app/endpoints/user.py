from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.user import UserController
from app.config.database import SessionLocal, engine
import app.models.user as model_user
import app.schemas.user as schema_user
import app.libs.utils.jwt as jwt


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

model_user.Base.metadata.create_all(bind=engine)
user_controller = UserController()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def read_users(
    db: Session = Depends(get_db),
    role: int = None,
    skip: int = 0,
    limit: int = 1000,
):
    results = user_controller.get_users(db=db, role=role, skip=skip, limit=limit)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Users not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": [user.as_dict_user() for user in results],
        "detail": {
            "message": "Successfully get users",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.post("/")
async def create_user(
    user: schema_user.User, 
    db: Session = Depends(get_db)
):
    results = user_controller.create_user(db=db, user=user)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "user already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )
        
    response_content = {
        "data": results.as_dict_user(),
        "detail": {
            "message": "Successfully added user",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user: schema_user.User,
    db: Session = Depends(get_db)
):
    results = user_controller.update_user(db=db, user_id=user_id, user=user)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "user not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    if results == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "user already exists",
                "status_code": status.HTTP_409_CONFLICT,
            },
        )    
    
    response_content = {
        "data": results.as_dict_user(),
        "detail": {
            "message": "Successfully updated user",
            "status_code": status.HTTP_200_OK,
        },
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    results = user_controller.delete_user(db=db, user_id=user_id)
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "user not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
    
    response_content = {
        "data": results.as_dict_user(),
        "detail": {
            "message": "Successfully deleted user",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

@router.post("/login")
async def login_user(
    login: schema_user.Login,
    db: Session = Depends(get_db)
):
    results = user_controller.login_user(db=db, username=login.username, password=login.password)
    
    if results == 401:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "password is incorrect",
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        )
    
    if results == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "user not found",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
        )
        
    subject = {
        "user_id": results.user_id,
        "username": results.username,
        "name": results.name,
        "position": results.position,
        "role": results.role,
    }    
    
    response_content = {
        "access_token": jwt.create_access_token(user_id=subject["user_id"], username=subject["username"], name=subject["name"], position=subject["position"], role=subject["role"]),
        "user_id": subject["user_id"],
        "username": subject["username"],
        "name": subject["name"],
        "position": subject["position"],
        "role": subject["role"],
        "detail": {
            "message": "Successfully login user",
            "status_code": status.HTTP_200_OK,
        },
    }
    
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK
)
