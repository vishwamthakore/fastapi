from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

app = FastAPI()

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
    return {"data": my_posts}

@app.post("/posts")
def create_post(post : Post):
    global id
    id = id + 1
    new_post =  {
        "id" : id,
        "title" : post.title,
        "content" : post.content
        }
    
    my_posts.append(new_post)
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    
    if post is None:
        return JSONResponse({"message" : "not found"}, 404)        
        
    else:
        return {"data" : post}

@app.delete("/posts/{id}")
def delete_post(id : int):
    index = get_post_index(id)

    if index is not None:
        deleted = my_posts.pop(index)
        return JSONResponse({"data" : deleted}, 204)

    else:
        return JSONResponse({"message" : "not found"}, 404)

@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    index = get_post_index(id)
    
    if index is not None:
        updated_post = post.model_dump()
        updated_post["id"] = id
        my_posts[index] = updated_post

        return JSONResponse({"data" : my_posts[index]}, 200)








