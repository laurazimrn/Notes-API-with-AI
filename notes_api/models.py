from sqlalchemy import Column, Integer, String
from notes_api.database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    conteudo = Column(String)

