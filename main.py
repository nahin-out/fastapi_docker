from fastapi import Depends, FastAPI, HTTPException, Query
from models import UserProfile
from db_crud import create_db_and_tables, get_session
from typing import Annotated
from sqlmodel import Session, create_engine, select
from update_model import UserProfileBase
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()
app.add_event_handler("startup", create_db_and_tables)
def on_startup():
    create_db_and_tables()

@app.post("/create_new_user")

def create_userprofile(userprofile: UserProfile,session: SessionDep) -> UserProfile:
    session.add(userprofile)
    session.commit()
    session.refresh(userprofile)
    return userprofile

@app.get("/show_all_profiles")
def show_all_profile(session: SessionDep,
                     offset: int = 0,
                        limit: Annotated[int, Query(le=100)] = 100,
                        ) -> list[UserProfile]:
    user_profiles =session.exec(select(UserProfile).offset(offset).limit
    (limit)).all()
    return user_profiles

@app.get('/userprofiles/{user_id}')
def show_user_profile(user_id: int, session: SessionDep)-> UserProfile:
    user_profile = session.get(UserProfile, user_id)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_profile


@app.put('/userprofile/{user_id}')
def userprofile_update(user_id:int, user_update: UserProfileBase, session:
    SessionDep)-> UserProfile:
        user_profile = session.get(UserProfile, user_id)
        if user_profile is None:
            raise HTTPException(status_code=404, detail="User not found")
        update_data= user_update.dict(exclude_unset=True)
        for ls -akey, value in update_data.items():
            setattr(user_profile, key, value)
        session.commit()
        session.refresh(user_profile)
        
        return user_profile
    
@app.delete('/userprofile/{user_id}')
def delete_profile(user_id: int, session: SessionDep):
    user_profile= session.get(UserProfile, user_id)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_profile)
    session.commit()
    return {"Ok, deleted": True}
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")