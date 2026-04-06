from subprocess import HIGH_PRIORITY_CLASS
from typing import List, Optional
from sqlmodel import SQLModel, Field

class CursoModel(SQLModel, table=True):
    __tablename__ = "cursos"
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    aulas: int
    horas: int