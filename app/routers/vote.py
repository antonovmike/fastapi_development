from fastapi import Depends, HTTPException, status, APIRouter

router = APIRouter(
    prefix="/vote",
    tags=['Vote'] # Adds headers to documentation http://127.0.0.1:8000/redoc
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote():
    pass