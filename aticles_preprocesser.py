import re
from functools import reduce
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import pdfplumber


def pdf_to_str(path):
    """
    Parse pdf to str
    :param path: pdf' path
    :return: pdf' context as str
    """

    with pdfplumber.open(path) as pdf:
        text = reduce(lambda doc, page: doc+page.extract_text(x_tolerance=0, y_tolerance=0), pdf.pages)
    return text


def remove_special_characters(text):
    """
    Leave only letters and numbers (maybe it's better to remove numbers?)
    :param text: input str
    :return: str with only letters and numbers
    """
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex, '', text)
    return text


def lemmatize_words(words, wordlemmatizer):  # Maybe try to use stemming
    """Lemmatize words taking into account part of speach"""
    lemmatized_words = []
    for word, pos in words:
        lemmatized_words.append(wordlemmatizer.lemmatize(word, get_wordnet_pos(pos)))
    return lemmatized_words


def get_wordnet_pos(treebank_tag):
    """Rename parts of speach for lemmatization"""

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return 'n'


def preprocess_text(text, wordlemmatizer=WordNetLemmatizer(), stopwords=set(stopwords.words('english'))):
    """
    Preprocess paper text (remove spacial characters and stop words, lower the text and lemmatize it)
    :param text: paper text
    :param wordlemmatizer: wordlemmatizer
    :param stopwords: delete these words from text
    :return:
    """
    text = remove_special_characters(str(text))
    text = re.sub(r'\d+', '', text)  # remove digits
    tokenized_words_with_stopwords = word_tokenize(text)
    tokenized_words = [word for word in tokenized_words_with_stopwords if word not in stopwords]
    tokenized_words = [word for word in tokenized_words if len(word) > 1]
    tokenized_words = [word.lower() for word in tokenized_words]
    tokenized_words_with_pos = pos_tag(tokenized_words)
    lemmatized_words = lemmatize_words(tokenized_words_with_pos, wordlemmatizer)
    return ' '.join(lemmatized_words)
