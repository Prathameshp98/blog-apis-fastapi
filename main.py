from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):

    if published:
        return { 'data' : f'Blog is published with limit {limit}'}
    else:
        return { 'data' : f'Blog is not published with limit {limit}'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}')
def blogs(id: int):
    return {'data' : id}

@app.get('/blog/{id}/comments')
def comments(id):
    return { 'data' : { id : 'some comment'}}


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]  

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'Post is created with title {request.title}'}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)