import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    user_password = Column(String, nullable=False)

    key = relationship("Key", back_populates="user")
    passwords = relationship("Password", back_populates="user")


class Key(Base):
    __tablename__ = 'key'
    key_id = Column(Integer, primary_key=True)
    key_value = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    user = relationship("User", back_populates="key")
    passwords = relationship("Password", back_populates="key")

class Password(Base):
    __tablename__ = 'passwords'
    password_id = Column(Integer, primary_key=True)
    site = Column(String, nullable=False)
    password_value = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)

    key_id = Column(Integer, ForeignKey('key.key_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    key = relationship("Key", back_populates="passwords")
    user = relationship("User", back_populates="passwords")

class Database:
    def __init__(self, db_url="sqlite:///password_manager.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
