from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

from schemas.artigo_schema import ArtigoSchema

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        from_attributes = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str = Field(..., min_length=4, max_length=72)

class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=4, max_length=72)
    eh_admin: Optional[bool] = None