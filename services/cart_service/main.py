from fastapi import FastAPI, HTTPException, Request
from strawberry.fastapi import GraphQLRouter

import strawberry

from services.auth_utils import decode_access_token


app = FastAPI()

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization").split()[1]
    try:
        payload = decode_access_token(token)
        request.state.user = payload["id"]
    except HTTPException as e:
        raise e

    response = await call_next(request)
    return response


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, info) -> str:
        return f"Hello {info.context['request'].state.user}!"

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
