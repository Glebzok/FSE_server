import argparse
import os
import pickle
from scipy.sparse import vstack as vstack_sparse

from aticles_preprocesser import pdf_to_str, preprocess_text
from articles_parser import get_all_papers, index_papers
from datasets_finder import get_papers_to_dataset
from vectorizer import train_vectorizer
from datasets_finder import extract_evaluation_part


def reinit_articles_base(papers_data_path, pdf_papers_path, download_years=None, download_papers_per_year=None):
    """
       Reinitialize the papers database (parse all papers from https://proceedings.neurips.cc,
       index them, than a vectotizer and create a dataset-paper index)
    :param papers_data_path: path to papers data (save all data here)
    :param pdf_papers_path: relative from papers_data_path path to papers pdf (save pdf files here)
    :param download_years: how many years' data to parse starting from the 1987, if None download all years data
    :param download_papers_per_year: how many papers per year to load, if None download all years' papers
    """
    get_all_papers(papers_data_path, download_years, download_papers_per_year)
    index_papers(papers_data_path, os.path.join(papers_data_path, pdf_papers_path))
    train_vectorizer(papers_data_path)
    get_papers_to_dataset(papers_data_path)


# don't update datasets currently
def add_articles(papers_data_path, new_papers_path, pdf_papers_path, preprocessed_papers_path):
    """
        Add new articles to current articles base (adds all papers from new_papers_path to papers base and deletes them)
    :param papers_data_path: path to papers data (save all data here)
    :param new_papers_path: relative from papers_data_path path to new papers pdfs (add all papers from here)
    :param pdf_papers_path: relative from papers_data_path path to papers pdf (save pdf files here)
    :param preprocessed_papers_path: relative from papers_data_path path to papers preprocessed texts
    """
    if not os.path.exists(os.path.join(papers_data_path, new_papers_path)):
        os.mkdir(os.path.join(papers_data_path, new_papers_path))

    with open(os.path.join(papers_data_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    with open(os.path.join(papers_data_path, 'tfidf_vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)

    with open(os.path.join(papers_data_path, 'tfidf_matrix.pkl'), 'rb') as f:
        tfidf_data, words = pickle.load(f)

    with open(os.path.join(papers_data_path, 'dataset_with_articles.pkl'), 'rb') as f:
        dataset_with_articles = pickle.load(f)

    with open(os.path.join(papers_data_path, 'wiki_datasets.pkl'), 'rb') as f:
        datasets = pickle.load(f)

    # index to new papers to start
    max_ind = max(papers_index.keys()) + 1

    for i, paper in enumerate(os.listdir(os.path.join(papers_data_path, new_papers_path))):
        paper_id = max_ind + i
        paper_name = paper.replace('.pdf', '')
        papers_index[paper_id] = paper_name
        paper_str = preprocess_text(pdf_to_str(os.path.join(papers_data_path, new_papers_path, paper)))

        with open(os.path.join(papers_data_path, preprocessed_papers_path, paper_name + '.txt'), 'w') as f:
            f.write(paper_str)

        # update tfidf
        article_tfidf = vectorizer.transform([paper_str])
        tfidf_data = vstack_sparse([tfidf_data, article_tfidf])

        # move paper from new_papers_path to pdf path
        os.rename(os.path.join(papers_data_path, new_papers_path, paper),
                  os.path.join(papers_data_path, pdf_papers_path, paper))

        if type(paper_str) == str:
            evaluation_text = extract_evaluation_part(paper_str, papers_data_path)

            if evaluation_text is not None:
                evaluation_text = evaluation_text.lower()

                for dataset in datasets:
                    search_dataset_in_paper = evaluation_text.find(dataset)

                    if search_dataset_in_paper != -1:
                        dataset_with_articles[dataset].append(paper_id)

    with open(os.path.join(papers_data_path, 'papers_index.pkl'), 'wb') as f:
        pickle.dump(papers_index, f)

    with open(os.path.join(papers_data_path, 'tfidf_matrix.pkl'), 'wb') as f:
        pickle.dump([tfidf_data, words], f)

    with open(os.path.join(papers_data_path, 'dataset_with_articles.pkl'), 'wb') as f:
        pickle.dump(dataset_with_articles, f)


if __name__ == '__main__':

    papers_data_path = './papers_data'

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", help='parse # of years data, if not specified then parse all',
                        action='store', default=None)
    parser.add_argument("-a", help='parse # of articles per year, if not specified then parse all',
                        action='store', default=None)
    parser.add_argument("-r", help='reinit articles base if the flag is specified, otherwise add new papers'
                        , action='store_true')

    if parser.parse_args().r:
        n_years = int(parser.parse_args().y)
        n_articles_per_year = int(parser.parse_args().a)
        reinit_articles_base(papers_data_path, 'pdf', n_years, n_articles_per_year)

    else:
        add_articles(papers_data_path, 'new_papers', 'pdf', 'preprocessed_papers')
