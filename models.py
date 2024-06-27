from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Specify the database URL. It'll be created by first run
DATABASE_URL = "sqlite:///./test.db"

# Create db engine
engine = create_engine(DATABASE_URL)

# Create a class for making local sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        index=True
        )
    first_name = Column(
        String,
        index=True
    )
    last_name = Column(
        String,
        index=True
    )
    email = Column(
        String,
        unique=True,
        index=True
    )
    password = Column(
        String
    )

    books = relationship(
        "Book",
        back_populates="user"
    )


class Book(Base):
    __tablename__ = 'books'

    id = Column(
        Integer,
        primary_key=True,
        index=True
        )
    title = Column(
        String,
        index=True
        )
    author = Column(
        String,
        index=True
        )
    genre = Column(
        String,
        index=True
        )
    user_id = Column(
        Integer,
        ForeignKey('users.id')
        )
    review_url = Column(
        String
        )

    user = relationship(
        "User",
        back_populates="books"
        )
