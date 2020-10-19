from tqdm import tqdm
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def preprocessed_papers_to_list(main_path):
    res = []

    with open(os.path.join(main_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    for paper_id, paper_name in tqdm(sorted(zip(papers_index.keys(),
                                                papers_index.values()))):
        with open(os.path.join(main_path, 'preprocessed_papers',
                               paper_name + '.txt'), 'r') as f:
            res.append(f.read())
    return res


def train_vectorizer(main_path):
    preprocessed_papers_list = preprocessed_papers_to_list(main_path)

    vectorizer = TfidfVectorizer()  # Convert all characters to lowercase before tokenizing
    tfidf_data = vectorizer.fit_transform(preprocessed_papers_list)
    words = vectorizer.get_feature_names()

    with open(os.path.join(main_path, 'tfidf_matrix.pkl'), 'wb') as f:
        pickle.dump((tfidf_data, words), f)

    with open(os.path.join(main_path, 'tfidf_vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)

    return tfidf_data, words, vectorizer


def transform_vectorizer(main_path):
    pass
