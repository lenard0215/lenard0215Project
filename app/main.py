from fastapi import FastAPI, Depends
from httpcore import Origin
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#------------------------------------------------------------------------------------------------------------------------------------------------------------
my_post = [{"title": "title of post 1", "content":" content of Post 1", "id": 1}, {"title": "favorite food", "content": "I like pizza", "id": 2}]

def find_post(id:int):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index_post(id):

    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
#------------------------------------------------------------------       
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": " Hello World!!!!... How are you", "id": 2}

#----------------------------------------------------------------------------
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
#__________________________________________________________________________________________________
