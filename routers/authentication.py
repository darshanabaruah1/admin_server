from fastapi import APIRouter,Depends,status,HTTPException
from routers import schemas
import database,models
from sqlalchemy.orm import Session
from routers import Hash


router=APIRouter(tags=['Authentication'])


@router.post('/register')
def register(request:schemas.Register,db: Session=Depends(database.get_db)):
    new_user = db.query(models.User).filter(
        models.User.email == request.email).first()
    if new_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Already Exists")
    else:
        new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message":"user successfully created"}

@router.post('/login')
def login(request:schemas.Login,db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    return user
