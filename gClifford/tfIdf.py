#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def tfIdf(corpus):
    """Compute the tf-idf matrix for the corpus. Corpus should be a list of string.  """
    vectorizer = CountVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus)
    counts = X.toarray()
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(counts)
    return tfidf
