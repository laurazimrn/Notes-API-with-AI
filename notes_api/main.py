from fastapi import FastAPI
from notes_api.database import Base, engine
from notes_api.routes import notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API with Ollama")
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "API de Análise"}
