from app.core.ai import client
from app.services.ai_service import AiService

ai_manager=AiService(ai=client)

def get_ai_service():
    return ai_manager