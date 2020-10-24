import os
import pickle
import requests
import json
from tqdm import tqdm
from bs4 import BeautifulSoup

from aticles_preprocesser import preprocess_text


def get_full_paper_data(main_url, abstract_add_url,
                        pdf_folder, bibtex_folder, metadata_folder, preprocessed_paper_folder):
    """
    Download paper in pdf format, bibtex file, metadata and preprocessed text for a given paper
    :param main_url: neurips proceedings main page url
    :param abstract_add_url: papers abstract url suffix
    :param pdf_folder: path to pdf files to save
    :param bibtex_folder: path to bibtex files to save
    :param metadata_folder: path to metadata files to save
    :param preprocessed_paper_folder: path to preprocessed papers texts to save
    """

    abstract_response = requests.get(main_url + abstract_add_url, allow_redirects=True)

    paper_name = (BeautifulSoup(abstract_response.text, 'html.parser')
                  .find_all('h4')[0].text
                  .replace('/', '_')
                  .replace('\\', '_')
                  .replace(' ', '_'))

    files_add_load_url = abstract_add_url.replace('hash', 'file')

    paper_add_load_url = files_add_load_url.replace('Abstract.html', 'Paper.pdf')
    paper_response = requests.get(main_url + paper_add_load_url, allow_redirects=True)
    open(os.path.join(pdf_folder, paper_name + '.pdf'), 'wb').write(paper_response.content)

    bibtex_add_load_url = files_add_load_url.replace('Abstract.html', 'Bibtex.bib')
    bibtex_response = requests.get(main_url + bibtex_add_load_url, allow_redirects=True)
    open(os.path.join(bibtex_folder, paper_name + '.bib'), 'wb').write(bibtex_response.content)

    metadata_add_load_url = files_add_load_url.replace('Abstract.html', 'Metadata.json')
    metadata_response = requests.get(main_url + metadata_add_load_url, allow_redirects=True)
    open(os.path.join(metadata_folder, paper_name + '.json'), 'wb').write(metadata_response.content)

    preprocessed_paper_text = preprocess_text(json.loads(metadata_response.content)['full_text'])
    open(os.path.join(preprocessed_paper_folder, paper_name + '.txt'), 'w').write(preprocessed_paper_text)


def get_one_year_papers(main_url, add_year_url,
                        pdf_folder, bibtex_folder, metadata_folder, preprocessed_papers_folder,
                        download_papers_per_year=None):
    """
    Parse all papers for a given year from https://proceedings.neurips.cc and save papers in pdf format, bibtex
    files, metadata and preprocessed papers text
    :param main_url: main_url: neurips proceedings main page url
    :param add_year_url: year' papers url suffix
    :param pdf_folder: path to pdf files to save
    :param bibtex_folder: path to bibtex files to save
    :param metadata_folder: path to metadata files to save
    :param preprocessed_papers_folder: path to preprocessed papers texts to save
    :param download_papers_per_year: # of papers per year to download
    :return:
    """

    res = requests.get(main_url + add_year_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    abstracts_add_url = [i.a['href'] for i in soup.find_all('ul')[1].find_all('li')]

    if download_papers_per_year is not None:
        abstracts_add_url = abstracts_add_url[:download_papers_per_year]

    for abstract_add_url in tqdm(abstracts_add_url, leave=False, desc='Papers'):
        get_full_paper_data(main_url, abstract_add_url,
                            pdf_folder, bibtex_folder, metadata_folder, preprocessed_papers_folder)


def get_all_papers(save_dir='./test_papers', n_download_years=None, n_download_papers_per_year=None):
    """
    Parse all papers from https://proceedings.neurips.cc and save papers in pdf format, bibtex
    files, metadata and preprocessed papers text
    :param save_dir: path to papers data (save all data here)
    :param n_download_years: # how many years' data to parse starting from the 1987, if None download all years data
    :param n_download_papers_per_year: how many papers per year to load, if None download all years' papers
    """
    main_url = 'https://proceedings.neurips.cc'
    main_response = requests.get(main_url)

    pdf_folder = os.path.join(save_dir, 'pdf')
    bibtex_folder = os.path.join(save_dir, 'bibtex')
    metadata_folder = os.path.join(save_dir, 'metadata')
    preprocessed_papers_folder = os.path.join(save_dir, 'preprocessed_papers')

    for path in (save_dir, pdf_folder, bibtex_folder, metadata_folder, preprocessed_papers_folder):
        if not os.path.exists(path):
            os.mkdir(path)

    add_year_urls = sorted([i.a['href'] for i in BeautifulSoup(main_response.text, 'html.parser')
                           .find_all('div', 'col-sm')[0]
                           .find_all('li')])
    if n_download_years is not None:
        add_year_urls = add_year_urls[:n_download_years]
    for add_year_url in tqdm(add_year_urls, leave=False, desc='Years'):
        get_one_year_papers(main_url, add_year_url,
                            pdf_folder, bibtex_folder, metadata_folder, preprocessed_papers_folder,
                            n_download_papers_per_year)


def index_papers(save_dir, papers_dir):
    """
    Add all papers from papers_dir to index
    :param save_dir: path to papers data (all data is saved here)
    :param papers_dir: path to papers pdfs
    """
    papers_index = {ind: paper[:-4] for ind, paper in enumerate(os.listdir(papers_dir))}
    with open(os.path.join(save_dir, 'papers_index.pkl'), 'wb') as f:
        pickle.dump(papers_index, f)
    return papers_index
