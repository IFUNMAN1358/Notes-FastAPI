from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.postgres.engine import get_db
from app.postgres.tables import Note
from app.schemas import users
from app.schemas import notes
from app.security.auth import get_current_user


router = APIRouter()


# ================================================================
# Get notes
# ================================================================


@router.get('/', status_code=200)
async def get_notes(db: AsyncSession = Depends(get_db),
                    current_user: users.ReturnIdUser = Depends(get_current_user)):
    query = await db.execute(select(Note).where(Note.owner_id == current_user.id))
    list_notes = query.scalars().all()
    if len(list_notes) == 0:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='You dont have notes'
        )
    return list_notes


# ================================================================
# Create and delete note
# ================================================================


@router.post('/create_note', response_model=notes.ReturnNote, status_code=201)
async def create_note(input_note: notes.CreateNote,
                      db: AsyncSession = Depends(get_db),
                      current_user: users.ReturnIdUser = Depends(get_current_user)):
    note = await db.scalar(select(Note).where(and_(Note.title == input_note.title, Note.owner_id == current_user.id)))
    if note:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='You already have a note with this title'
        )

    note = Note(owner_id=current_user.id,
                title=input_note.title,
                content=input_note.content)
    db.add(note)
    await db.commit()
    return note


@router.delete('/delete_note/{note_id}', response_model=notes.ReturnNote, status_code=200)
async def delete_note(note_id: int,
                      db: AsyncSession = Depends(get_db),
                      current_user: users.ReturnIdUser = Depends(get_current_user)):
    note = await db.scalar(select(Note).where(and_(Note.id == note_id, Note.owner_id == current_user.id)))
    if note is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Note not found'
        )
    await db.delete(note)
    await db.commit()
    return note


# ================================================================
# Update and make favorite note
# ================================================================


@router.put('/update_note/{note_id}', response_model=notes.ReturnNote, status_code=200)
async def update_note(note_id: int,
                      input_note: notes.CreateNote,
                      db: AsyncSession = Depends(get_db),
                      current_user: users.ReturnIdUser = Depends(get_current_user)):
    note = await db.scalar(select(Note).where(and_(Note.id == note_id, Note.owner_id == current_user.id)))
    if note is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Note not found'
        )
    if note.title == input_note.title:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='You already have a note with this title'
        )

    note.title = input_note.title
    note.content = input_note.content
    await db.commit()
    return note


@router.post('/favorite/{note_id}', response_model=notes.ReturnNote, status_code=201)
async def make_favorite(note_id: int,
                        db: AsyncSession = Depends(get_db),
                        current_user: users.ReturnIdUser = Depends(get_current_user)):
    note = await db.scalar(select(Note).where(and_(Note.id == note_id, Note.owner_id == current_user.id)))
    if note is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Note not found'
        )
    note.is_favorite = not note.is_favorite
    await db.commit()
    return note
