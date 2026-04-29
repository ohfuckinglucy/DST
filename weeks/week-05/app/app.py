import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Profile:
    id: strawberry.ID
    name: str
    phone: str

db = []

@strawberry.type
class Query:
    @strawberry.field
    def profiles(self) -> list[Profile]:
        return db

    @strawberry.field
    def profile(self, id: strawberry.ID) -> Profile | None:
        return next((p for p in db if p.id == id), None)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_profile(self, name: str, phone: str) -> Profile:
        new_profile = Profile(id=strawberry.ID(str(len(db) + 1)), name=name, phone=phone)
        db.append(new_profile)
        return new_profile

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
