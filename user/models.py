from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_staff = Column(Boolean, default=False)

class BlackListToken(Base):
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(500), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='blacklist_tokens')
    jti = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())