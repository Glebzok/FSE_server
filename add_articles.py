from nltk import download
import argparse
import os
import pickle
from scipy.sparse import vstack as vstack_sparse

from aticles_preprocesser import pdf_to_str, preprocess_text


def reinit_articles_base(main_path, test=False):
    get_all_papers(main_path, test)
    index_papers(main_path, os.path.join(main_path, 'pdf'))
    train_vectorizer(main_path)


def add_articles(main_path, new_papers_path, pdf_path, preprocessed_paper_folder):
    with open(os.path.join(main_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    with open(os.path.join(main_path, 'tfidf_vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)

    with open(os.path.join(main_path, 'tfidf_matrix.pkl'), 'rb') as f:
        tfidf_data, words = pickle.load(f)

    max_ind = max(papers_index.keys()) + 1

    for i, paper in enumerate(os.listdir(os.path.join(main_path, new_papers_path))):
        paper_id = max_ind + i
        paper_name = paper.replace('.pdf', '')
        papers_index[paper_id] = paper_name
        paper_str = preprocess_text(pdf_to_str(os.path.join(main_path, new_papers_path, paper)))

        with open(os.path.join(main_path, preprocessed_paper_folder, paper_name + '.txt'), 'w') as f:
            f.write(paper_str)

        article_tfidf = vectorizer.transform([paper_str])
        tfidf_data = vstack_sparse([tfidf_data, article_tfidf])

        os.rename(os.path.join(main_path, new_papers_path, paper),
                  os.path.join(main_path, pdf_path, paper))

    with open(os.path.join(main_path, 'papers_index.pkl'), 'wb') as f:
        pickle.dump(papers_index, f)

    with open(os.path.join(main_path, 'tfidf_matrix.pkl'), 'wb') as f:
        pickle.dump([tfidf_data, words], f)


download('wordnet')
download('stopwords')
download('punkt')
download('averaged_perceptron_tagger')

main_path = './papers_data'

from articles_parser import get_all_papers, index_papers
from vectorizer import train_vectorizer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help='test mode', action='store_true')
    parser.add_argument("-r", help='reinit articles base', action='store_true')

    if parser.parse_args().r:
        if parser.parse_args().t:
            reinit_articles_base(main_path, True)
        else:
            reinit_articles_base(main_path, False)

    else:
        add_articles(main_path, 'new_papers', 'pdf', 'preprocessed_papers')
