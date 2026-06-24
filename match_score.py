from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

resume_text = """
python java c c++ html css sql dbms data structures algorithms
oop linux ubuntu oracle web development
"""

job_description = """
Looking for a Python developer with SQL, Linux,
Data Structures, Algorithms, Git and Docker experience.
"""

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(
    [resume_text, job_description]
)

score = cosine_similarity(
    vectors[0:1],
    vectors[1:2]
)[0][0]

print("ATS Score:", round(score * 100, 2), "%")