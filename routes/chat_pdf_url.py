from fastapi import APIRouter, Depends
from apis.chat_pdf import chat_with_pdf, generate_flash_cards_from_pdf, generate_quiz_from_pdf, load_and_vectorize_file, summerize_pdf
from config import Settings
from deps import get_settings

router = APIRouter(prefix="/pdf", tags={"PDF"})


# Get text summerized
@router.get('/summarize/{temp_file_path:path}')
def get_summary(temp_file_path: str,  settings: Settings = Depends(get_settings)):
    summary = summerize_pdf(tempfile_path=temp_file_path,
                            openai_key=settings.openai_api_key)
    return summary

# Get Quizzes and anwswers
@router.get('/quiz/{url:path}')
def get_quiz_and_anwsers(url: str,  settings: Settings = Depends(get_settings)):
    quizes = generate_quiz_from_pdf(
        url=url, pinecone_key=settings.pinecone_api_key, openai_api_key=settings.openai_api_key)
    return quizes

# Get flashcards
@router.get('/flashcards/{url:path}')
def get_flash_cards(url: str,  settings: Settings = Depends(get_settings)):
    flascards = generate_flash_cards_from_pdf(
        url=url, pinecone_key=settings.pinecone_api_key, openai_api_key=settings.openai_api_key)
    return flascards

# Load the url
@router.get('/load/{url:path}')
def load_pdf(url: str,  settings: Settings = Depends(get_settings)):
    results = load_and_vectorize_file(
        url, pinecone_key=settings.pinecone_api_key, openai_api_key=settings.openai_api_key)
    return results

# Chat with the pdf
@router.post('/chat/{url:path}/{query}')
def chat_with_the_pdf(query: str, url: str, chat_history: list | None = [],  settings: Settings = Depends(get_settings)):
    bot_message = chat_with_pdf(
        query=query, url=url, chat_history=chat_history, pinecone_key=settings.pinecone_api_key, openai_api_key=settings.openai_api_key)
    return bot_message
