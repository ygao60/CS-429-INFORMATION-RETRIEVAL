"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
from collections import defaultdict
import io
import math

import numpy as np


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        Each iteration consists of calls to compute_means and compute_clusters.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector)
        See Log.txt for expected output.
        """
        self.doc_norm=defaultdict(lambda:0)
        self.docu=documents
        doc_id=0
        for doc in documents:
            norm=0
            for term in doc:
                norm+=math.pow(doc[term],2)
            self.doc_norm[doc_id]=norm 
            doc_id+=1
        self.mean_vectors=[]
        for i in range(self.k):
            self.mean_vectors.append(documents[i])
        self.mean_norms=[]
        for doc in self.mean_vectors:
            norm=0
            for term in doc:
                norm+=math.pow(doc[term],2)
            self.mean_norms.append(norm)
        for j in range(iters):
            self.compute_clusters(documents)
            self.compute_means()
            
            num_of_docs=[]
            for i in self.cluster_doc:
                num_of_docs.append(len(self.cluster_doc[i]))
            print num_of_docs
            print self.error(documents)
            
        

            
    def compute_means(self):
        """ Compute the mean vectors for each cluster (storing the results in an
        instance variable)."""
     
        del self.mean_vectors[:]
        for i in range(self.k):
            c=Counter()
            l=0
            for doc_id in self.cluster_doc[i]:
                c.update(self.docu[doc_id])
                l+=1
            if (l!=0):
                for doc in c:
                    c[doc]=1.0*c[doc]/l
            self.mean_vectors.append(c)
        self.mean_norms=[]
        for doc in self.mean_vectors:
            norm=0
            for term in doc:
                norm+=math.pow(doc[term],2)
            self.mean_norms.append(norm)
        

    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable). """
        
            
        self.cluster_doc=defaultdict(list) 
        doc_id=0
        for doc in documents:
            for i in range(self.k):
                dis=self.distance(doc,self.mean_vectors[i],self.mean_norms[i]+self.doc_norm[doc_id])
                if (i==0):
                   min=i
                   min_dis=dis
                else:
                    if (dis<min_dis):
                        min=i
                        min_dis=dis
            self.cluster_doc[min].append(doc_id)
            doc_id+=1
            

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        dis=mean_norm
        for term in doc:
            dis+=-2.0*doc[term]*mean[term]
        return math.sqrt(dis)
        

    def error(self, documents):
        """ Return the error of the current clustering, defined as the sum of the
        Euclidean distances between each document and its assigned mean vector."""
        error=0
        self.cluster_doc_dis=defaultdict(list)
        for cluster in self.cluster_doc:
            for doc_id in self.cluster_doc[cluster]:
                doc=documents[doc_id]
                d=self.distance(doc,self.mean_vectors[cluster],self.mean_norms[cluster]+self.doc_norm[doc_id])
                error+=d
                self.cluster_doc_dis[cluster].append((doc,d))
        return error
        

    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster, sorted by distance to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (which will be out of order from the original
        document).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        for i in self.cluster_doc:
            print "CLUSTER %d" %i
            top=sorted(self.cluster_doc_dis[i],key=lambda x:x[1])
            k=0
            j=0
            while (j<n and k<len(top)):
                if(len(top[k][0])>3):
                    print top[k][0].keys()
                    j+=1
                k+=1
                
            


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    mark=defaultdict(lambda:0)
    delete=defaultdict(lambda:0)
    copy=[]
    count=0
    l=len(docs)
    for doc in docs:
        new_doc=Counter()
        for term in doc:
            if (delete[term]==0):
                if (mark[term]==1):
                    new_doc.update({term:doc[term]})     
                else:
                    mark[term]=1
                    df=0
                    for i in range(count,l):
                        if term in docs[i]:
                            df+=1
                            if (df>=min_df):
                                new_doc.update({term:doc[term]}) 
                                break
                    if (df<min_df):
                        delete[term]=1
        count+=1
        copy.append(new_doc)
    return [doc for doc in copy if doc]
            


def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with io.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles


def main():
    """ DO NOT MODIFY. """
    profiles = read_profiles('profiles.txt')
    print 'read', len(profiles), 'profiles.'
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
