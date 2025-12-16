from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.routers.services.recommendations import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

service = RecommendationService()

@router.get("/user/{user_id}")
def recommend_for_user(user_id: int, db: Session = Depends(get_db)):
    recs = service.recommend_for(user_id, db)
    # повернемо списком dict (JSON)
    return [
        {
            "id": m.id,
            "title": m.title,
            "genre": m.genre,
            "year": m.year,
            "rating": m.rating,
            "description": m.description
        }
        for m in recs
    ]
