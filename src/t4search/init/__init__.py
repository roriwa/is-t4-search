# -*- coding=utf-8 -*-
r"""

"""
import logging
import nltk
import chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2


def __main__():
    logging.info("Initializing dependencies")

    logging.info("downloading nltk")
    nltk.download("punkt_tab", raise_on_error=True)

    logging.info("downloading onnx")
    embedder = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
    # noinspection PyUnresolvedReferences,PyProtectedMember
    embedder._download_model_if_not_exists()
