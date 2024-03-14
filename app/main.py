from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import psycopg2
import psycopg2.extras

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

    # cur.execute("SELECT * FROM posts;")
    # t = cur.fetchone()
    # print(dict(t))

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
    

@app.get("/")
async def home():
    return {"data": "Hello World"}


@app.get("/posts")
async def get_posts():
    cur.execute("SELECT * FROM POSTS;")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts")
def create_post(post : Post):
    cur.execute(f"""INSERT INTO POSTS (TITLE, CONTENT) VALUES ('{post.title}', '{post.content}') returning *""")
    new_post = cur.fetchone()
    con.commit()
    return {"data" : new_post}


@app.get("/posts/{id}")
def get_post(id : int):
    cur.execute(f"SELECT * FROM POSTS WHERE ID = {id};")
    post = cur.fetchone()

    if post is None:
        return JSONResponse({"message" : "not found"}, 404)        
    else:
        return {"data" : post}
    

@app.delete("/posts/{id}")
def delete_post(id : int):
    cur.execute(f"DELETE FROM POSTS WHERE ID = {id} returning *")
    post = cur.fetchone()
    con.commit()
    
    if post is not None:
        return JSONResponse({"data" : post}, 204)
    else:
        return JSONResponse({"message" : "not found"}, 404)
    

@app.put("/posts/{id}")
def update_post(id : int, post : Post):

    cur.execute(f"""UPDATE POSTS SET title = '{post.title}', content = '{post.content}' WHERE ID = {id} returning *""")
    post = cur.fetchone()
    con.commit()

    if post is not None:
        return JSONResponse({"data" : post}, 200)
    else:
        return JSONResponse({"message" : "not found"}, 404)


