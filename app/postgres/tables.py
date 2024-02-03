from uuid import uuid4

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, UUID, Integer, Boolean, ForeignKey


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship('Note', back_populates='owner')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    content = Column(String)
    tag = Column(String, index=True)
    is_favorite = Column(Boolean, default=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    owner = relationship('User', back_populates='notes')