from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session


router = APIRouter()

#Post - Criar um novo curso
@router.post('/', response_model=CursoSchema, status_code=status.HTTP_201_CREATED)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()
    await db.refresh(novo_curso)
    return novo_curso

#Get - Listar todos os cursos
@router.get('/', response_model=List[CursoSchema], status_code=status.HTTP_200_OK)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos = result.scalars().all()
        return cursos

#Get - Buscar um curso por ID
@router.get('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session )):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
        return curso

# Put - Atualizar um curso por ID
@router.put('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def put_curso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        if curso_up is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
        curso_up.titulo = curso.titulo
        curso_up.aulas = curso.aulas
        curso_up.horas = curso.horas
        await session.commit()
        await session.refresh(curso_up)
        return curso_up

# Delete - Excluir um curso por ID
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del = result.scalar_one_or_none()
        if curso_del is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
        await session.delete(curso_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
