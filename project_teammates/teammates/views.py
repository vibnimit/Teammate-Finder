from django.shortcuts import render
from project_teammates.settings import nltk_dir, BASE_DIR
from teammates.models import Course
# Create your views here.

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# from wordcloud import WordCloud
# url = project_teammates.settings.nltk_dir
import nltk
nltk.data.path.append(nltk_dir)
# import nltk.data
from nltk.corpus import subjectivity, stopwords, wordnet, sentiwordnet
from nltk import word_tokenize, pos_tag
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer

# import ast
# import json
import re

# from nltk.stem.porter import PorterStemmer

import contractions
# from textblob import TextBlob, Word
# from multiprocessing import Process
import json

#load all libraries
import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy
import string
import contractions


STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang)) for lang in nltk.corpus.stopwords.fileids()}

nlp = spacy.load(BASE_DIR + '/en/en_core_web_sm')
def get_data(reviews):
    def clean_comments(text):
        #remove punctuations
        regex = re.compile('[' + re.escape(string.punctuation) + '\\r\\t\\n]')
        nopunct = regex.sub(" ", str(text))

        nopunct = contractions.fix(nopunct)

        nopunct = nopunct.lower()

        #use spacy to lemmatize comments
        doc = nlp(nopunct, disable=['parser','ner'])
        lemma = [token.lemma_ for token in doc]
        return lemma


    def rightTypes(ngram):
        if '-pron-' in ngram or '' in ngram  or '-PRON-' in ngram or ' -PRON-' in ngram or ' 'in ngram or 't' in ngram:
            return False
        for word in ngram:
            if word in en_stopwords:
                return False
        acceptable_types = ('JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS')
        second_type = ('NN', 'NNS', 'NNP', 'NNPS')
        tags = nltk.pos_tag(ngram)
        if tags[0][1] in acceptable_types and tags[1][1] in second_type:
            return True
        else:
            return False


    # reviews = ["He is a good programmer, knows java and python well.", "He is intelligent and supportive, help others in the team to work", " Lazy, do not attend the meeting, never on time. No contribution to the project"]
    lemmatized = clean_comments(reviews)

    # print(lemmatized)

    bigrams = nltk.collocations.BigramAssocMeasures()


    bigramFinder = nltk.collocations.BigramCollocationFinder.from_words(lemmatized)

    bigram_freq = bigramFinder.ngram_fd.items()

    bigramFreqTable = pd.DataFrame(list(bigram_freq), columns=['bigram','freq']).sort_values(by='freq', ascending=False)

    bigramFreqTable.head().reset_index(drop=True)

    en_stopwords = set(stopwords.words('english'))

    filtered_bi = bigramFreqTable[bigramFreqTable.bigram.map(lambda x: rightTypes(x))]

    bgram = filtered_bi['bigram'].values
    freq = filtered_bi['freq'].values

    dict = {}

    i = 0
    for val in bgram:
        if ' ' not in val[0] and ' ' not in val[1]:
          dict[val[0] + "-" + val[1]] = freq[i]
        i += 1

    print(dict)
    return dict




def populateCourses():
    fp = open(BASE_DIR + "/courses.txt")
    coursesList = fp.readlines()
    for course in coursesList:
        code, name = course.split("::")
        course_obj, created = Course.objects.update_or_create(code=code, name=name)
    fp.close()