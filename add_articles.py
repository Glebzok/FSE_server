from nltk import download
import argparse
import os
import pdfplumber

def reinit_articles_base(main_path, test=False):

    get_all_papers(main_path, True)
    index_papers(main_path, os.path.join(main_path, 'pdf'))
    train_vectorizer(main_path)

def add_articles(main_path, new_papers_path):
    for paper in os.listdir(os.path.join(main_path, new_papers_path)):


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

    if 'r' in parser.parse_args():
        if 't' in parser.parse_args():
            reinit_articles_base(main_path, True)
        else:
            reinit_articles_base(main_path, False)

