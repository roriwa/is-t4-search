# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pydantic import BaseModel


__all__ = ['MongoDelegatedModel']


class MongoDelegatedModel(BaseModel):
    id: str
    # biographie
    fraktion: t.Optional[str]
    nachname: str
    vorname: str
    titel: str
    # wahlperiode
