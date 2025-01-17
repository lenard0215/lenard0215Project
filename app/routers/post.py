
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_description= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user), limit: int = 10, skip: int=0,
                 search: Optional[str] =""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                            isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print (results)
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000000)
    #my_post.append(post_dict)

    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
                    #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
                    
    #new_post = models.Post(title =post.title, content= post.content, published=post.published)
    id: int = current_user.id
    #print(id)
    new_post = models.Post(owner_id =id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):

#post = find_post(id)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} not found")   
              
    return current_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):

#index= find_index_post(id)
#my_post.pop(index)    
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post{id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized")

    deleted_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_description= schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query =db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

#index= find_index_post(id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post{id} does not exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized")
#post_dict = post.dict()
#post_dict['id'] = id
#my_post[index] = post_dict
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()