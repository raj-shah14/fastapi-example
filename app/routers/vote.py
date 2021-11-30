from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from .. import schemas, database, oauth2, models

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post doesn't exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                    models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f" User {current_user.id} has already voted on post: {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return { "message": "Vote Added Successfully"} 
    else:
        if not found_vote:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Vote doesn't exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return { "Message":"Successfully deleted Vote"}