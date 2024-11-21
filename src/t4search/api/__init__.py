# -*- coding=utf-8 -*-
r"""

"""
import fastapi


api = fastapi.FastAPI(title="T4Search API")


@api.get("/")
def index():
    return {'message': "Hello World!"}


def __main__(**kwargs):
    import uvicorn, configlib
    uvicorn.run(app=api, **configlib.config.get('api', fallback={}), **kwargs)
