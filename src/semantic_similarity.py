from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
import re


@st.cache_resource
def load_word2vec_model():
    model_path = "data/GoogleNews-vectors-negative300.bin"

    model =  KeyedVectors.load_word2vec_format(
        model_path , binary=True
    )



    return model




def get_word_vector(text , model):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    vectors = []

    for word in words:
        if word in model:
            vectors.append(model[word])

    if not vectors:
        return None

    return np.mean(vectors, axis=0)

def calculate_semantic_similarity(resume_text, job_text):
    model = load_word2vec_model()

    resume_vector = get_word_vector(resume_text, model)
    job_vector = get_word_vector(job_text, model)

    if resume_vector is None or job_vector is None:
        return 0.0

    similarity = cosine_similarity(
        [resume_vector],
        [job_vector]
    )[0][0]

    return float(similarity * 100)
