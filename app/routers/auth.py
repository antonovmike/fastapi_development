from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database

router = APIRouter(tags=['Authentification'])


@router.post('/login')
def login(db: Session = Depends(database.get_db)):
    pass
