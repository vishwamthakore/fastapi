from fastapi import FastAPI
from fastapi import Request, Depends
from fastapi import Response
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import psycopg2
import psycopg2.extras
from .database import engine, SessionLocal, get_db
from . import models
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    pg_connection_dict = {
        'dbname': 'fastapi',
        'user': 'postgres',
        'password': '09061995',
        'port': 5432,
        'host': 'localhost'
    }

    print(pg_connection_dict)
    con = psycopg2.connect(**pg_connection_dict)
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    print(con)


except Exception as e:
    print(f'Exception : {e}')

class Post(BaseModel):
    title : str
    content : str


id = 1
my_posts = [
    {
        "id" : 1,
        "title" : "title for post 1",
        "content" : "content for post 1"
    }
]

def find_post(id):
    for p in my_posts:
        if p.get("id") == id:
            return p
        
def get_post_index(id):
    for i,p in enumerate(my_posts):
        if p.get("id") == id:
            return i

@app.get("/test")
def test(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
async def home():
    return {"data": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts")
def create_post(post : Post, db: Session = Depends(get_db)):

    post = models.Post(title = post.title, content = post.content)
    print(post.__dict__)
    db.add(post)
    db.commit()

    db.refresh(post)
    return {"data" : post}


@app.get("/posts/{id}")
def get_post(id : int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if post is None:
        return JSONResponse({"message" : "not found"}, 404)        
    else:
        return {"data" : post}


@app.delete("/posts/{id}")
def delete_post(id : int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is not None:
        post.delete()
        db.commit()
        return JSONResponse({"data" : "deleted"}, 204)
    else:
        return JSONResponse({"message" : "not found"}, 404)
    

@app.put("/posts/{id}")
def update_post(id : int, post : Post, db: Session = Depends(get_db)):

    curr_post_query = db.query(models.Post).filter(models.Post.id == id)
    curr_post = curr_post_query.first()

    if curr_post is not None:
        print(post.model_dump())
        curr_post_query.update(post.model_dump())
        db.commit()
        return {"data" : curr_post_query.first()}
    else:
        return JSONResponse({"message" : "not found"}, 404)


