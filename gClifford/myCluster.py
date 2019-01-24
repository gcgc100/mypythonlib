#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle

from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import DBSCAN
from sklearn.cluster import Birch

import tfIdf

class myCluster(object):
    """This is my base cluster. Define basic methods. The other cluster inherit it."""

    def __init__(self):
        super(myCluster, self).__init__()

    def items():
        doc = "The items property."
        def fget(self):
            return self._items
        def fset(self, value):
            self._items = value
        def fdel(self):
            del self._items
        return locals()
    items = property(**items())

    def generateCorpus(self):
        """Generate corpus for cluster. Return a dict. The key is the original item, value is the string."""
        raise NotImplementedError()

#    def KMeansCluster(self, n_clusters):
#        """Run Cluster"""
#        self.preProcess()
#        corpus = self.generateCorpus()
#        vectors = tfIdf.tfIdf(corpus)
#        pickle.dump(vectors, open("tfidf.p", "wb"))
#        est = KMeans(n_clusters = n_clusters)
#        est.fit(vectors)
#        self.postProcess(est)
#        return est

    def cluster(self, n_clusters, min_samples = 1, cluster = None, vectorizer = None):
        """Run cluster"""
        def vectorizerDefault():
            """vectorizer callback func"""
            corpus = self.generateCorpus()
            self.items = corpus.keys()
            vectors = tfIdf.tfIdf(corpus.values())
            pkl = {"items": self.items, "vectors": vectors}
            pickle.dump(pkl, open("vectors.p", "wb"))
            return vectors
        vectorizer = vectorizer or vectorizerDefault
        cluster = cluster or myCluster.KMeansCluster
        self.preProcess()
        vectors = vectorizer()
        est = cluster(n_clusters = n_clusters, vectors = vectors, min_samples = min_samples)
        self.postProcess(est)
        return est

    @classmethod
    def KMeansCluster(self, n_clusters, vectors, **kw):
        """Cluster the vectors directly"""
        est = KMeans(n_clusters = n_clusters)
        est.fit(vectors)
        return est

    @classmethod
    def MeanShiftCluster(self, n_clusters, vectors, **kw):
        """Cluster the vectors with MeanShift algorithm"""
        bandwidth = estimate_bandwidth(vectors.toarray(), quantile=0.2, n_samples=10)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(vectors.toarray())
        return ms
        
    @classmethod
    def DBSCANCluster(self, n_clusters, vectors, min_samples=1, **kw):
        """Cluster the vectors with DBSCAN algorithm"""
        db = DBSCAN(eps = 0.3, min_samples=int(min_samples)).fit(vectors.toarray())
        return db

    @classmethod
    def BirchCluster(self, n_clusters, vectors, **kw):
        """Cluster the vectors with Birch algorithm"""
        brc = Birch(n_clusters = n_clusters).fit(vectors.toarray())
        return brc

    def preProcess(self):
        """Do some work before cluster"""
        pass

    def postProcess(self, est):
        """Do some work after cluster"""
        pass
