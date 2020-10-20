from aticles_preprocesser import preprocess_text
import numpy as np
import pickle
import os


def get_best_matching_articles_idx(search_query,
                                   tfidf_matrix_path='./papers_data/tfidf_matrix.pkl',
                                   tfidf_vectorizer_path='./papers_data/tfidf_vectorizer.pkl'):
    preprocessed_search_text = preprocess_text(search_query)

    with open(tfidf_matrix_path, 'rb') as f:
        tfidf_matrix, words = pickle.load(f)

    with open(tfidf_vectorizer_path, 'rb') as f:
        tfidf_vectorizer = pickle.load(f)

    search_matrix = tfidf_vectorizer.transform([preprocessed_search_text]).reshape(-1, 1)
    np_search_matrix = tfidf_matrix @ search_matrix
    np_search_matrix = np_search_matrix.toarray().flatten()

    return np.argsort(np_search_matrix)[::-1]


def get_search_query_response(search_query, main_path='./papers_data', n=20):
    best_matching_articles_idx = get_best_matching_articles_idx(search_query)

    with open(os.path.join(main_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    best_matching_articles_names = [papers_index[paper_idx] for paper_idx in best_matching_articles_idx[:n]]

    response = {'result': [{'name': paper_name.replace('_', ' '),
                            'link': paper_name + '.pdf'} for paper_name in best_matching_articles_names]}

    return response
