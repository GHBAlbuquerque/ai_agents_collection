from pydantic import BaseModel, Field
from agent.models import MovieRecommendation

class RecommendationRequest(BaseModel):
    preferences: str = Field(description="User preferences on movies", min_length=10, max_length=500)
    
class RecommendationResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was succcesful")
    data: MovieRecommendation = Field(..., description="")
    message: str = Field(default="Recommendations sucessfully generated", description="Informative message")