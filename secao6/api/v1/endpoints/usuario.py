from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioSchemaArtigos
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

#Get Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
  return usuario_logado


#Post / Signup
@router.post('/signup', response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
  novo_usuario = UsuarioModel(
    nome=usuario.nome,
    sobrenome=usuario.sobrenome,
    email=usuario.email,
    senha=gerar_hash_senha(usuario.senha),
    eh_admin=usuario.eh_admin
  )
  async with db as session:
    session.add(novo_usuario)
    await session.commit()
    return novo_usuario

#Get Usuarios
@router.get('/', response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_usuarios(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel)
    result = await session.execute(query)
    usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
    return usuarios

#Get Usuario por ID
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await session.execute(query)
    usuario: Optional[UsuarioSchemaArtigos] = result.scalars().unique().one_or_none()
    if usuario is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')
    return usuario

#Put Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario_atualizado: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await session.execute(query)
    usuario: Optional[UsuarioModel] = result.scalars().unique().one_or_none()
    if usuario is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')

    usuario.nome = usuario_atualizado.nome
    usuario.sobrenome = usuario_atualizado.sobrenome
    usuario.email = usuario_atualizado.email
    if usuario_atualizado.senha:
      usuario.senha = gerar_hash_senha(usuario_atualizado.senha)

    await session.commit()
    return usuario

#Delete Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await session.execute(query)
    usuario: Optional[UsuarioModel] = result.scalars().unique().one_or_none()
    if usuario is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')

    await session.delete(usuario)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Post Login
@router.post('/login',  status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
  usuario = await autenticar(db, form_data.username, form_data.password)
  if not usuario:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email ou senha incorretos')

  token_acesso = criar_token_acesso(sub=usuario.id)
  return JSONResponse(content={'access_token': token_acesso, 'token_type': 'bearer'})
