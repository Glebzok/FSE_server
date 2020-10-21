import os
import pickle
from collections import defaultdict
from tqdm import tqdm
import json


def check_symbols_before_eval_name(cut_paper_text, eval_name_index):
    possible_number = cut_paper_text[eval_name_index - 2]
    possible_space = cut_paper_text[eval_name_index - 1]

    return possible_number.isdigit() and possible_space == ' '


def extract_evaluation_part(paper_text, main_path, cut_size=0.5):
    cut_index = int(cut_size * len(paper_text))
    cut_paper_text = paper_text[cut_index:]

    with open(os.path.join(main_path, 'evaluation_names.pkl'), 'rb') as f:
        eval_names = pickle.load(f)

    eval_name_index = -1

    for eval_name in eval_names:
        eval_name_index = cut_paper_text.find(eval_name + '\n')

        if eval_name_index != -1:
            if check_symbols_before_eval_name(cut_paper_text, eval_name_index):
                break

    if eval_name_index != -1:
        references_index = cut_paper_text.find('References')

        if references_index == -1:
            return cut_paper_text[eval_name_index:]
        else:
            return cut_paper_text[eval_name_index:references_index]

    else:
        return None


def get_papers_to_dataset(main_path):
    with open(os.path.join(main_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    with open(os.path.join(main_path, 'datasets.pkl'), 'rb') as f:
        datasets = pickle.load(f)

    # datasets = ['MNIST',
    #             'VisualQA',
    #             'Visual-QA'
    #             'WordNet',
    #             'titanic',
    #             'iris',
    #             'imagenet',
    #             'hoba',
    #             'Machine Translation of Various Languages',
    #             'IMDB Reviews',
    #             'Twenty Newsgroups',
    #             'Sentiment140',
    #             'MS-COCO',
    #             'The Wikipedia Corpus']

    dataset_with_articles = defaultdict(list)

    for paper_id, paper_name in tqdm(sorted(zip(papers_index.keys(),
                                                papers_index.values()))):

        with open(os.path.join(main_path, 'metadata',
                               paper_name + '.json'), 'r') as f:
            paper_text = json.load(f)['full_text']

        evaluation_text = extract_evaluation_part(paper_text, main_path)
        for dataset in datasets:

            if evaluation_text is not None:
                search_dataset_in_paper = evaluation_text.find(dataset.lower())

                if search_dataset_in_paper != -1:
                    dataset_with_articles[dataset].append(paper_id)

    with open(os.path.join(main_path, 'dataset_with_articles.pkl'), 'wb') as f:
        pickle.dump(dataset_with_articles, f)
