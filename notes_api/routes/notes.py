from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notes_api.database import SessionLocal
from notes_api.models import Note as NoteModel
from notes_api.schemas import NoteCreate, Note
import ollama


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/notes/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = NoteModel(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# READ ALL
@router.get("/notes/", response_model=list[Note])
def read_notes(db: Session = Depends(get_db)):
    return db.query(NoteModel).all()

# READ ONE
@router.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return note

# UPDATE
@router.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note_update: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    note.titulo = note_update.titulo
    note.conteudo = note_update.conteudo
    db.commit()
    db.refresh(note)
    return note

# DELETE
@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    db.delete(note)
    db.commit()
    return {"message": "Nota deletada com sucesso"}

@router.get("/notes/{note_id}/summary")
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    try:
        response = ollama.chat(model="llama3.2", messages=[
            {"role": "user", "content": f"Resuma o seguinte texto em poucas linhas: {note.conteudo}"}
        ])
        resumo = response["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")

    return {
        "id": note.id,
        "titulo": note.titulo,
        "resumo": resumo
    }

