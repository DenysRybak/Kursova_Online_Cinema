from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, models
from backend.database import get_db
from backend.routers.services.recommendations import RecommendationService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -----------------------------
# Create new user (Register)
# -----------------------------
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password=user.password,   # поки без шифрування
        subscription_type=user.subscription_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# -----------------------------
# Get all users
# -----------------------------
@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# -----------------------------
# Get user by ID
# -----------------------------
@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -----------------------------
# Login
# -----------------------------
@router.post("/login", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return db_user

# -----------------------------
# Update subscription type
# -----------------------------
@router.patch("/{user_id}/subscription")
def update_subscription(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sub = data.get("subscription_type")
    if sub not in ["free", "premium"]:
        raise HTTPException(status_code=400, detail="Invalid subscription type")

    user.subscription_type = sub
    db.commit()
    db.refresh(user)
    return {"status": "ok", "subscription": sub}


# -----------------------------
# Delete user
# -----------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}



@router.get("/{user_id}/recommendations")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    service = RecommendationService()
    movies = service.recommend_for(user_id, db)
    return movies
