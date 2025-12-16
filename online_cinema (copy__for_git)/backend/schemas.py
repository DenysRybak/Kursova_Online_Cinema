from pydantic import BaseModel

# ---- MOVIE SCHEMAS ----

class MovieCreate(BaseModel):
    title: str
    genre: str
    year: int
    country: str
    rating: str
    description: str

class Movie(MovieCreate):
    id: int

    class Config:
        from_attributes = True

# -------------------------
# USERS
# -------------------------

class UserBase(BaseModel):
    username: str
    subscription_type: str | None = "free"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# -------------------------
# FAVORITES
# -------------------------

class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    class Config:
        from_attributes = True

