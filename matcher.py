## This script uses sklearn to match resumes to job descriptions using TF-IDF and cosine similarity.

#Currently, it matches the resume to the top 2 job descriptions based on cosine similarity.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_jobs(resume_text, job_descriptions):
    documents = [resume_text] + job_descriptions
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    matches = list(zip(job_descriptions, similarity_scores))
    matches.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 2 matches; CHANGE LATER
    return matches[:2]
