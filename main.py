from fastapi import FastAPI
from routes import apis_urls, chat_pdf_url

import config

settings = config.Settings()
app = FastAPI()

app.include_router(apis_urls.router)
app.include_router(chat_pdf_url.router)



@app.get("/")
def root():
    return {
        "message": f"Welcome to version {settings.api_version} of our Study API"
    }
