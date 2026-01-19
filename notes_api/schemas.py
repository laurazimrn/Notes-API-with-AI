from pydantic import BaseModel, ConfigDict

class NoteBase(BaseModel):
    titulo: str
    conteudo: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # substitui orm_mode
