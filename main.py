from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import Base, engine, SessionLocal, User as UserModel, Book as BookModel
from schema import schema
from pydantic import BaseModel
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
import bcrypt

app = FastAPI()

templates = Jinja2Templates(directory='templates')

Base.metadata.create_all(bind=engine)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    user_id: int
    review_url: str


@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookModel(
        title=book.title,
        author=book.author,
        genre=book.genre,
        user_id=book.user_id,
        review_url=book.review_url
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/htmx/books", response_class=HTMLResponse)
async def get_books_via_graphql(request: Request):
    query = """
    {
        allBooks {
            title
            author
            user {
                firstName
                lastName
            }
        }
    }
    """
    result = schema.execute(query)
    # TODO testing
    print(result)
    books = result.data["allBooks"]
    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "books": books
            }
        )

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
