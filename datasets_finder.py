import os
import pickle
from collections import defaultdict
from tqdm import tqdm
import json


def check_symbols_before_eval_name(cut_paper_text, eval_name_index):
    """
    Checks that there is the number of section before the evaluation section title.
    Usually every section in a paper looks like: "5. Evaluation", so we this pattern
    :param cut_paper_text: possible evaluation section of the paper
    :param eval_name_index: possible index of evaluation section title
    :return: True if the pattern is satisfied
    """
    possible_number = cut_paper_text[eval_name_index - 2]
    possible_space = cut_paper_text[eval_name_index - 1]

    return possible_number.isdigit() and possible_space == ' '


def extract_evaluation_part(paper_text, paper_data_path, cut_size=0.5):
    """
    Extract the evaluation part from the paper' text
    :param paper_text: paper text
    :param paper_data_path: path to papers data
    :param cut_size: what portion of the text to cut off, before looking for evaluation section
    :return: evaluation section text
    """
    cut_index = int(cut_size * len(paper_text))
    cut_paper_text = paper_text[cut_index:]

    with open(os.path.join(paper_data_path, 'evaluation_names.pkl'), 'rb') as f:
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


def get_papers_to_dataset(paper_data_path):
    """
    Get datasets-papers index
    :param paper_data_path:  path to papers data
    """
    with open(os.path.join(paper_data_path, 'papers_index.pkl'), 'rb') as f:
        papers_index = pickle.load(f)

    with open(os.path.join(paper_data_path, 'wiki_datasets.pkl'), 'rb') as f:
        datasets = pickle.load(f)

    datasets = [dataset.lower() for dataset in datasets]
    dataset_with_articles = defaultdict(list)

    for paper_id, paper_name in tqdm(sorted(zip(papers_index.keys(),
                                                papers_index.values()))):
        try:
            with open(os.path.join(paper_data_path,
                                   'metadata',
                                   paper_name + '.json'), 'rb') as f:
                paper_text = json.load(f)['full_text']
        except Exception as e:
            print(e)
            continue

        if type(paper_text) == str:
            evaluation_text = extract_evaluation_part(paper_text)

            if evaluation_text is not None:
                evaluation_text = evaluation_text.lower()

                for dataset in datasets:
                    search_dataset_in_paper = evaluation_text.find(dataset)

                    if search_dataset_in_paper != -1:
                        dataset_with_articles[dataset].append(paper_id)

    with open(os.path.join(paper_data_path, 'dataset_with_articles.pkl'), 'wb') as f:
        pickle.dump(dataset_with_articles, f)
