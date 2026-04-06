from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from models.curso_models import CursoModel
from core.deps import get_session

#Bypass warning SqlModel select
from sqlmodel.sql.expression import select, SelectOfScalar, Select

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
#Fim Bypass

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
  novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
  db.add(novo_curso)
  await db.commit()
  return novo_curso

#Get all cursos
@router.get("/", response_model=List[CursoModel])
async def get_curso(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel)
    result = await session.execute(query)
    cursos: List[CursoModel] = result.scalars().all()
    return cursos

#Get curso by id
@router.get("/{curso_id}", response_model=CursoModel, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == curso_id)

        result = await session.execute(query)

        curso: Optional[CursoModel] = result.scalar_one_or_none()

        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado"
            )

        return curso

#Update curso
@router.put("/{curso_id}", response_model=CursoModel, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == curso_id)
    result = await session.execute(query)
    curso_up: CursoModel = result.scalar_one_or_none()
    if not curso_up:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    curso_up.titulo = curso.titulo
    curso_up.aulas = curso.aulas
    curso_up.horas = curso.horas
    await session.commit()
    return curso_up

#Delete curso

@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == curso_id)
    result = await session.execute(query)
    curso: CursoModel = result.scalar_one_or_none()
    if not curso:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    await session.delete(curso)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)