from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from pydantic_core import Url
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from models import artigo_model
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema

from core.deps import get_session, get_current_user

router = APIRouter()

# Post Artigo
@router.post("/", status_code=HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel= Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo,
        conteudo=artigo.conteudo,
        url_fonte=artigo.url_fonte,
        usario_id=usuario_logado.id
    )
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo

# Get Artigos
@router.get("/", status_code=HTTP_200_OK, response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().all()
        return artigos

# Get Artigo by ID
@router.get("/{artigo_id}", status_code=HTTP_200_OK, response_model=ArtigoSchema)
async def get_artigo_by_id(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).where(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().first()
        if not artigo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")
        return artigo

# Put Artigo
@router.put("/{artigo_id}", status_code=HTTP_200_OK, response_model=ArtigoSchema)
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, usuario_logado: UsuarioModel= Depends(get_current_user),
                     db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).where(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().first()
        if not artigo_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")
        if artigo_up.usario_id != usuario_logado.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado para atualizar este artigo")
        artigo_up.titulo = artigo.titulo
        artigo_up.conteudo = artigo.conteudo
        artigo_up.url_fonte = artigo.url_fonte
        await session.commit()
        return artigo_up

# Delete Artigo
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, usuario_logado: UsuarioModel= Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).where(ArtigoModel.id == artigo_id).filter(ArtigoModel.usario_id == usuario_logado.id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().first()
        if not artigo_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")
        if artigo_del.usario_id != usuario_logado.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado para deletar este artigo")
        await session.delete(artigo_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)