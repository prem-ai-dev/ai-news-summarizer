from fastapi import APIRouter, Depends, Body
from fastapi.responses import StreamingResponse
from app.core.dependency import get_ai_service
from app.services.ai_service import AiService

router=APIRouter(prefix="/ai_service",tags=["AI"])

@router.post("/")
async def chat(content:str=Body(...),
               ai_manager:AiService=Depends(get_ai_service)):
    response=StreamingResponse(ai_manager.news_summaraizer(content=content),
                               media_type="text/event-stream")
    return response