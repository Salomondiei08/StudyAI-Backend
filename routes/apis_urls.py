from fastapi import APIRouter, Depends

from apis.chat_with_gpt import chat_with_ai_genius
from apis.google_scholars_api import get_articles
from apis.youtube_api import get_youtube_videos
from config import Settings
from deps import get_settings


router = APIRouter(tags=['API'])

# Talk with the chat
@router.post("/chat/{query}")
def talk_to_ai(query: str, chat_history: list = [], settings: Settings = Depends(get_settings)):
    ai_response = chat_with_ai_genius(
        query=query, chat_history=chat_history, openai_api_key=settings.openai_api_key)
    return ai_response


# Get articles
@router.get("/articles/{query}")
def get_articles_results(query: str, limit: int = 20, settings: Settings = Depends(get_settings)):
    articles = get_articles(query=query, limit=limit,
                            key=settings.serp_api_key)
    return articles


# Get videos
@router.get("/videos/{query}")
def get_videos_results(query: str, limit: int = 20,  settings: Settings = Depends(get_settings)):
    videos = get_youtube_videos(
        query=query, limit=limit, key=settings.youtube_api_key)
    return videos
