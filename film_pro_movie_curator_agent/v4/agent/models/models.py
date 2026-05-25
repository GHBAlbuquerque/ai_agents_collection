from pydantic import BaseModel, Field
from typing import Optional, List

class Cast(BaseModel):
    """Information about a cast member"""
    name: str = Field(..., description="Actor/Actress name")
    character: Optional[str] = Field(None, description="Name of the character played")


class Movie(BaseModel):
    """Structured model for movie data"""
    title: str = Field(..., description="Movie title")
    release_year: int = Field(..., description="Release year")
    director: str = Field(..., description="Main director")
    genres: List[str] = Field(..., description="Genre and subgenres")
    imdb_rating: float = Field(..., description="IMDB rating (focus on 7.5+)")
    duration_minutes: int = Field(..., description="Duration in minutes")
    primary_language: str = Field(..., description="Primary language")
    synopsis: str = Field(..., description="Brief and engaging synopsis")
    age_rating: str = Field(..., description="Age rating (e.g., PG, PG-13, 16, 18)")
    content_warnings: Optional[List[str]] = Field(None, description="Content warnings")
    cast: List[Cast] = Field(default_factory=list, description="Notable cast")
    poster_url: Optional[str] = Field(None, description="Poster URL")
    streaming_platforms: Optional[List[str]] = Field(None, description="Streaming platforms")
    recommendation_reason: str = Field(..., description="Brief explanation for the recommendation")


class MovieRecommendation(BaseModel):
    """Structured response with multiple recommendations"""
    movies: List[Movie] = Field(..., description="List of recommended movies (minimum of 5)")
    total_recommendations: int = Field(..., description="Total number of movies recommended")