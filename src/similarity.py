from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, job_description_text):

    documents = [resume_text, job_description_text]

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(matrix[0:1], matrix[1:2])

    return similarity_score[0][0]*100
