import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Book as BookModel, User as UserModel
from models import SessionLocal


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Book(SQLAlchemyObjectType):
    class Meta:
        model = BookModel


class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_books = graphene.List(Book)

    def resolve_all_users(self, info):
        session = SessionLocal()
        return session.query(UserModel).all()

    def resolve_all_books(self, info):
        session = SessionLocal()
        return session.query(BookModel).all()


schema = graphene.Schema(query=Query)
