from starlette.status import HTTP_403_FORBIDDEN
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit:int = 10, skip:int = 0, search: Optional[str] = ""):
    #  By making use of SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # By making use of ORM , layer between SQL and code, to talk to DB

    posts = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title,
    # post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(user_id=current_user.id, **post.dict()) # Unpacks the post into dictionary and puts in the format we want.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", [id])
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesn't exist")
    
    return post

@router.delete("/{id}")
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, [id])
    # deleted_post = cursor.fetchone()

    # connection.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized to delete!")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()

    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesn't exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized to Update!")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
