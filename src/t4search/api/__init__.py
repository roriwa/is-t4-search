# -*- coding=utf-8 -*-
r"""

"""
import fastapi
from pydantic import BaseModel


api = fastapi.FastAPI(title="T4Search API")


class IndexModel(BaseModel):
    message: str


@api.get("/", response_model=IndexModel)
def index() -> IndexModel:
    return IndexModel(message="Hello World!")


def __main__(**kwargs):
    import uvicorn, configlib
    uvicorn.run(app=api, **configlib.config.get('api', fallback={}), **kwargs)
