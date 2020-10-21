import argparse
import os
import pickle
from scipy.sparse import vstack as vstack_sparse

from aticles_preprocesser import pdf_to_str, preprocess_text
from datasets_finder import get_papers_to_dataset


def reinit_articles_base(main_path, download_years=None, download_papers_per_year=None):
    get_all_papers(main_path, download_years, download_papers_per_year)
    index_papers(main_path, os.path.join(main_path, 'pdf'))
    train_vectorizer(main_path)
    get_papers_to_dataset(main_path)

# don't update datasets currently
def add_articles(main_path, new_papers_path, pdf_path, preprocessed_paper_folder):
    if not os.path.exists(os.path.join(main_path, new_papers_path)):
        os.mkdir(os.path.join(main_path, new_papers_path))

    with open(os.path.join(main_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    with open(os.path.join(main_path, 'tfidf_vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle. load(f)

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

main_path = './papers_data'

from articles_parser import get_all_papers, index_papers
from vectorizer import train_vectorizer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", help='parse # of years data', action='store', default=None)
    parser.add_argument("-a", help='parse # of articles per year', action='store', default=None)
    parser.add_argument("-r", help='reinit articles base', action='store_true')

    if parser.parse_args().r:
        n_years = int(parser.parse_args().y)
        n_articles_per_year = int(parser.parse_args().a)
        reinit_articles_base(main_path, n_years, n_articles_per_year)

    else:
        add_articles(main_path, 'new_papers', 'pdf', 'preprocessed_papers')
