from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter

from services.auth_utils import decode_access_token
from services.database import Base, get_session, setup_database
from services.cart_service.repositories.cart_repository_impl import CartRepositoryImpl
from services.cart_service.graphql.schema import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    from services.database import engine

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization").split()[1]
    try:
        payload = decode_access_token(token)
        request.state.user = payload["id"]
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    response = await call_next(request)
    return response


async def get_context(db: Session = Depends(get_session)):
    return {"cart_repository": CartRepositoryImpl(db)}


graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
