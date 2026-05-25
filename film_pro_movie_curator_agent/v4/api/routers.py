from fastapi import APIRouter, HTTPException

from agent.core import get_recommendations
from agent.models.models import MovieRecommendation
from api.models.dtos import RecommendationRequest, RecommendationResponse

router = APIRouter()

@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Get movie recommendations",
    description="Generates personalized movie recommendations based on user preferences",
    tags=["Recommendations"]
)
async def get_recommentaions(request: RecommendationRequest) -> RecommendationResponse:
    try:
        recommendations: MovieRecommendation = await get_recommendations(request.preferences)
        
        if not recommendations:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate recommendations."
            )
            
        return RecommendationResponse(
            success=True, 
            data=recommendations,
            message= ""
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to process recommendations: {str(e)}"
        )