# -*- coding=utf-8 -*-
r"""

"""
import nltk
import chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2


def __main__():
    nltk.download("punkt_tab", raise_on_error=True)

    embedder = chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2.ONNXMiniLM_L6_V2()
    embedder._download_model_if_not_exists()
