from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db


@router.get('/blog', response_model = List[schemas.ShowBlog], tags = ['Blogs'])
def all(db:  Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', status_code = status.HTTP_201_CREATED, tags = ['Blogs'])
def create(request: schemas.Blog, db:  Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

 
@router.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED, tags = ['Blogs'])
def update(id, request: schemas.Blog, db:  Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'blog with {id} is not found.')

    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'


@router.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['Blogs'])
def destroy(id, db:  Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return {'details': f'blog with id {id} is deleted.'}



@router.get('/blog/{id}', status_code = 200, response_model = schemas.ShowBlog, tags = ['Blogs'])
def show(id, response: Response, db:  Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'blog with {id} is not found.')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'blog with {id} is not found.'}
    return blog