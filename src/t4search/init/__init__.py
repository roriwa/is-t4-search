# -*- coding=utf-8 -*-
r"""

"""
import logging
import nltk
from ..core import create_chroma_embedding_function


def __main__():
    logging.info("Initializing dependencies")

    logging.info("downloading nltk")
    nltk.download("punkt_tab", raise_on_error=True)

    logging.info("downloading onnx")
    embedder = create_chroma_embedding_function()
    # noinspection PyUnresolvedReferences,PyProtectedMember
    embedder._download_model_if_not_exists()
