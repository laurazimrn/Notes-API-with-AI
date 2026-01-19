# Notes API with AI (CRUD + Summarization)

This project is a **RESTful API** built with [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/) to manage notes. It supports full **CRUD operations** and integrates with [Ollama](https://ollama.com/) to generate **AI-powered summaries** of notes.
-----------------------------------------------------------------------
#Features 
- Create, read, update, and delete notes (CRUD).
- SQLite database with SQLAlchemy ORM.
- Pydantic v2 schemas for validation and serialization.
- AI integration: summarize note content using Ollama (`llama3` model).
- Automated tests with Pytest and FastAPI TestClient.
