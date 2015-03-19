""" Assignment 3

"""
from collections import defaultdict
import codecs
import math
import re
import matplotlib.pyplot as plt


class Index(object):

    def __init__(self, filename=None, champion_threshold=10):
        """ DO NOT MODIFY.
        Create a new index by parsing the given file containing documents,
        one per line. You should not modify this. """
        if filename:  # filename may be None for testing purposes.
            self.documents = self.read_lines(filename)
            stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
            self.inverted_index=self.create_inverted_index(stemmed_docs)
            self.doc_freqs = self.count_doc_frequencies(self.inverted_index)
            self.i_doc_freq=self.inverse_doc_freq(self.inverted_index,self.doc_freqs)
            self.tf_index=self.create_tf_index(stemmed_docs)
            self.index = self.create_tfidf_index(stemmed_docs, self.doc_freqs,self.tf_index)
            self.doc_lengths = self.compute_doc_lengths(self.index)
            self.champion_index = self.create_champion_index(self.index, champion_threshold)   
            self.doc_len=self.document_length(stemmed_docs)
            self.num_of_docs=self.number_of_documents(self.documents)
            self.average_doc_len=self.average_document_length(self.doc_len,self.num_of_docs)
            
           
    def number_of_documents(self,docs):
        return len(docs)
   
    def average_document_length(self,doc_len,num_of_docs):
        sum=0
        for doc_id in doc_len:
            sum+=doc_len[doc_id]
        return (1. *sum/num_of_docs)
   
    def document_length(self, docs):
        length=defaultdict(lambda:0)
        doc_id=1
        for doc in docs:
            length[doc_id]=len(doc)
            doc_id+=1
        return length
     
     
    def compute_doc_lengths(self, index):
        """
        Return a dict mapping doc_id to length, computed as sqrt(sum(w_i**2)),
        where w_i is the tf-idf weight for each term in the document.

        E.g., in the sample index below, document 0 has two terms 'a' (with
        tf-idf weight 3) and 'b' (with tf-idf weight 4). It's length is
        therefore 5 = sqrt(9 + 16).

        >>> lengths = Index().compute_doc_lengths({'a': [[0, 3]], 'b': [[0, 4]]})
        >>> lengths[0]
        5.0
        """
        length=defaultdict(lambda:0)
        for query_term, query_weight in index.items():
            for doc_id, doc_weight in index[query_term]:
                length[doc_id] += doc_weight**2
        for doc_id in length:
            length[doc_id]=math.sqrt(length[doc_id])
        return length

    def create_champion_index(self, index, threshold=10):
        """
        Create an in dex mapping each term to its champion list, defined as the
        documents with the K highest tf-idf values for that term (the
        threshold parameter determines K).

        In the example below, the champion list for term 'a' contains
        documents 1 and 2; the champion list for term 'b' contains documents 0
        and 1.

        >>> champs = Index().create_champion_index({'a': [[0, 10], [1, 20], [2,15]], 'b': [[0, 20], [1, 15], [2, 10]]}, 2)
        >>> champs['a']
        [[1, 20], [2, 15]]
        >>> champs['b']
        [[0, 20], [1, 15]]
        """
        champ=defaultdict(list)
        for term, term_weight in index.items():
            l=sorted(term_weight, key=lambda x: x[1],reverse=True)
            if len(l)<threshold:
                champ[term]=l
            else:
                champ[term]=l[:threshold]
        return champ

    def create_BM25_index(self,RSV_doc_freqs,k,b,average_doc_len,doc_len,tf_index):
        BM25_index=defaultdict(list)
        for term in tf_index:
            for doc_id, tf in tf_index[term]:
                BM25= RSV_doc_freqs[term]*(k+1)*tf/(k*((1-b)+(1.*b*doc_len[doc_id]/average_doc_len))+tf)
                BM25_index[term].append([doc_id,BM25])
        return BM25_index
        
    
    def create_tf_index(self,docs):
        tf_index=defaultdict(list)
        doc_id=1
        for doc in docs:
            tf={}
            tf=defaultdict(lambda:0, tf)
            for term in doc:
                tf[term]+=1
            for t in tf:
                tf_index[t].append([doc_id,tf[t]])
            doc_id+=1
        return tf_index
        
    def create_tfidf_index(self, docs, doc_freqs,tf_index):
        """
        Create an index in which each postings list contains a list of
        [doc_id, tf-idf weight] pairs. For example:

        {'a': [[0, .5], [10, 0.2]],
         'b': [[5, .1]]}

        This entry means that the term 'a' appears in document 0 (with tf-idf
        weight .5) and in document 10 (with tf-idf weight 0.2). The term 'b'
        appears in document 5 (with tf-idf weight .1).

        Parameters:
        docs........list of lists, where each sublist contains the tokens for one document.
        doc_freqs...dict from term to document frequency (see count_doc_frequencies).

        Use math.log10 (log base 10).

        >>> index = Index().create_tfidf_index([['a', 'b', 'a'], ['a']], {'a': 2., 'b': 1., 'c': 1.})
        >>> sorted(index.keys())
        ['a', 'b']
        >>> index['a']
        [[0, 0.0], [1, 0.0]]
        >>> index['b']  # doctest:+ELLIPSIS
        [[0, 0.301...]]
        """
        n=len(docs)
        tfidf_index=defaultdict(list)
        """"doc_id=1
        for doc in docs:
            tf={}
            tf=defaultdict(lambda:0, tf)
            for term in doc:
                tf[term]+=1
            for t in tf:
                tfidf=(1+math.log10(tf[t]))* (math.log10(1. * n/doc_freqs[t]))
                tfidf_index[t].append([doc_id,tfidf])
            doc_id+=1
        return tfidf_index"""
        
        for term in tf_index:
            for doc_id, tf in tf_index[term]:
                tfidf=(1+math.log10(tf))* self.i_doc_freq[term]
                tfidf_index[term].append([doc_id,tfidf])
        return tfidf_index
            
            
    def create_inverted_index(self, docs):
        inverted_index=defaultdict(list)
        doc_id=1
        for doc in docs:
            doc=list(set(doc))
            for term in doc:
                inverted_index[term].append(doc_id)
            doc_id+=1
        return inverted_index
        
    def inverse_doc_freq(self,inverted_index,doc_freqs):
        n=len(self.documents)
        freq=defaultdict(lambda:0)
        for term in inverted_index:
            freq[term]=math.log10(1. * n/doc_freqs[term])
        return freq
        

        
    def count_doc_frequencies(self, inverted_index):
        """ Return a dict mapping terms to document frequency.
        >>> res = Index().count_doc_frequencies([['a', 'b', 'a'], ['a', 'b', 'c'], ['a']])
        >>> res['a']
        3
        >>> res['b']
        2
        >>> res['c']
        1
        """
        freq=defaultdict(lambda:0)
        for term in inverted_index:
            freq[term]=len(inverted_index[term])
        return freq
        

    def query_to_vector(self, query_terms):
        """ Convert a list of query terms into a dict mapping term to inverse document frequency.
	using log(N / df(term)), where N is number of documents and df(term) is the number of documents
        that term appears in.
        Parameters:
        query_terms....list of terms
        """
        n=len(self.documents)
        vector=defaultdict(lambda:0)
        tf=defaultdict(lambda:0)
        for term in query_terms:
            tf[term]+=1
        for term in tf:
            if term not in self.doc_freqs.keys():
                vector[term]=0
            else:
                vector[term]=(1+math.log10(tf[term]))*(math.log10(1. * n/self.doc_freqs[term]))
        return vector

    def search_by_BM25(self,query,k,b):
        """"tokens=self.tokenize(query)
        tokens=self.stem(tokens)"""
        tokens=list(set(query))
        scores=defaultdict(lambda:0)
        """"BM25_index=self.create_BM25_index(self.RSV_doc_freqs,k,b,self.average_doc_len,self.doc_len,self.tf_index)"""
        """"for term in tokens:
            for doc_id, BM25 in BM25_index[term]:
                scores[doc_id] += BM25
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)"""
        for term in tokens:
            for doc_id, tf in self.tf_index[term]:
                scores[doc_id]+=self.i_doc_freq[term]*(k+1)*tf/(k*((1-b)+(1.*b*self.doc_len[doc_id]/self.average_doc_len))+tf)
        return sorted(scores, key=scores.get, reverse=True)
        
        
 
    def search_by_cosine(self, query_vector, index, doc_lengths):
        """
        Return a sorted list of doc_id, score pairs, where the score is the
        cosine similarity between the query_vector and the document. The
        document length should be used in the denominator, but not the query
        length (as discussed in class). You can use the built-in sorted method
        (rather than a priority queue) to sort the results.

        The parameters are:

        query_vector.....dict from term to weight from the query
        index............dict from term to list of doc_id, weight pairs
        doc_lengths......dict from doc_id to length (output of compute_doc_lengths)

        In the example below, the query is the term 'a' with weight
        1. Document 1 has cosine similarity of 2, while document 0 has
        similarity of 1.

        >>> Index().search_by_cosine({'a': 1}, {'a': [[0, 1], [1, 2]]}, {0: 1, 1: 1})
        [(1, 2), (0, 1)]
        """
        scores=defaultdict(lambda:0)
        for query_term, query_weight in query_vector.items():
            for doc_id,doc_weight in index[query_term]:
                scores[doc_id] += query_weight * doc_weight
        for doc_id in scores:
            scores[doc_id] /= doc_lengths[doc_id]
        return sorted(scores, key=scores.get, reverse=True)
        
        
    def search_by_RSV(self,query):
        """" tokens=self.tokenize(query)
        tokens=self.stem(tokens)"""
        tokens=list(set(query))
        scores=defaultdict(lambda:0)
        for term in tokens:
            for doc_id in self.inverted_index[term]:
                scores[doc_id]+=self.i_doc_freq[term]
        return sorted(scores, key=scores.get, reverse=True)
        
       
        
   
     
    def search(self, query, use_champions=False):
        """ Return a list of (document_id, score) pairs for documents matching the query. Assume that
        query is a single string, possible containing multiple words. Assume
        queries with multiple words are phrase queries. The steps are to:

        1. Tokenize the query (calling self.tokenize)
        2. Stem the query tokens (calling self.stem)
        3. Convert the query into an idf vector (calling self.query_to_vector)
        4. Compute cosine similarity between query vector and each document (calling search_by_cosine).

        Parameters:

        query...........raw query string, possibly containing multiple terms (though boolean operators do not need to be supported)
        use_champions...If True, Step 4 above will use only the champion index to perform the search.
        """
        """"tokens=self.tokenize(query)
        tokens=self.stem(tokens)"""
        query_vector=self.query_to_vector(query)
        if not use_champions:
            return self.search_by_cosine(query_vector,self.index,self.doc_lengths)
        else:
            return self.search_by_cosine(query_vector,self.champion_index,self.doc_lengths)

    def read_lines(self, filename):
        """ DO NOT MODIFY.
        Read a file to a list of strings. You should not need to modify
        this. """
        list=[]
        first=True
        for l in codecs.open(filename, 'r', 'utf-8').readlines():
            l1=l.strip()
            if(l1.startswith("*TEXT")):
                if(first):
                    s=""
                    first=False
                else:
                    list.append(s)
                    s=""
            elif(l1.startswith("*STOP")):
                list.append(s)
            elif(not l1.startswith("\n")):
                s=' '.join([s,l1])
        return list
                
            
            
        
 
        

    def tokenize(self, document):
        """ DO NOT MODIFY.
        Convert a string representing one document into a list of
        words. Retain hyphens and apostrophes inside words. Remove all other
        punctuation and convert to lowercase.

        >>> Index().tokenize("Hi there. What's going on? first-class")
        ['hi', 'there', "what's", 'going', 'on', 'first-class']
        """
        return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

    def stem(self, tokens):
        """ DO NOT MODIFY.
        Given a list of tokens, collapse 'did' and 'does' into the term 'do'.

        >>> Index().stem(['did', 'does', 'do', "doesn't", 'splendid'])
        ['do', 'do', 'do', "doesn't", 'splendid']
        """
        return [re.sub('^(did|does)$', 'do', t) for t in tokens]

        
def curve(results,rel,num):
    pre=defaultdict(list)
    recall=defaultdict(list)
    for query_id in results:
        l=len(rel[query_id])
        i=0
        count=0
        for doc_id in results[query_id]:
            i+=1
            if doc_id in rel[query_id]:
                count+=1
            pre[query_id].append(1.*count/i)
            recall[query_id].append(1.*count/l)
    pre_ave=[0]*20
    recall_ave=[0]*20
    for query_id in pre:
        for i in range(0,20):
            pre_ave[i]+=pre[query_id][i]
            recall_ave[i]+=recall[query_id][i]
    for i in range(0,20):
        pre_ave[i]=1.*pre_ave[i]/num
        recall_ave[i]=1.*recall_ave[i]/num
    plt.figure()
    plt.plot(recall_ave,pre_ave,'bo-')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall curve')
    plt.show()
    
        
def evaluation(results,rel,num):
    pre={}
    recall={}
    F1={}
    MAP={}
    for query_id in results:
        i=0
        count=0
        s=0
        for doc_id in results[query_id]:
            i+=1
            if doc_id in rel[query_id]:
                count+=1
                s+=1.*count/i
        pre[query_id]=1.*count/20.0
        recall[query_id]=1.*count/len(rel[query_id])
        if (count==0):
            F1[query_id]=0
        else:
            F1[query_id]=2.*pre[query_id]*recall[query_id]/(pre[query_id]+recall[query_id])
        MAP[query_id]=1.*s/len(rel[query_id])
    l=[]
    l.append(1.*sum(pre.values())/num)
    l.append(1.*sum(recall.values())/num)
    l.append(1.*sum(F1.values())/num)
    l.append(1.*sum(MAP.values())/num)
    return l
   
 
 
def read_rel(rel_file):
    dic=defaultdict(list)
    for l in codecs.open(rel_file, 'r', 'utf-8').readlines():
        l1=l.strip()
        if l1:
            array=[int(x) for x in l1.split()] 
            dic[array[0]]=array[1:]
    return dic
    
    
def read_query(query_file):
    list=[]
    first=True
    for l in codecs.open(query_file, 'r', 'utf-8').readlines():
        l1=l.strip()
        if(l1.startswith("*FIND")):
            if(first):
                s=""
                first=False
            else:
                list.append(s)
                s=""
        elif(l1.startswith("*STOP")):
            list.append(s)
        elif(l1):
            s=' '.join([s,l1])
    return list


def main():
    """ DO NOT MODIFY.
    Main method. Constructs an Index object and runs a sample query. """
    indexer = Index('time/TIME.ALL')
    query2=read_query('time/TIME.QUE')
    query1=[]
    for query in query2:
        tokens=indexer.tokenize(query)
        tokens=indexer.stem(tokens)
        query1.append(tokens)
        
    query_id=1
    rel_cosine=defaultdict(list)   
    for query in query1:
        rel_cosine[query_id]=indexer.search(query)[:20]
        query_id+=1
    
    query_id=1
    rel_RSV=defaultdict(list)    
    for query in query1:
        rel_RSV[query_id]=indexer.search_by_RSV(query)[:20]
        query_id+=1
    
    query_id=1
    rel_BM25_1=defaultdict(list)   
    k=1.0
    b=0.5
    for query in query1:
        rel_BM25_1[query_id]=indexer.search_by_BM25(query,k,b)[:20]
        query_id+=1
    
    query_id=1
    rel_BM25_2=defaultdict(list)   
    k=1.0
    b=1.0
    for query in query1:
        rel_BM25_2[query_id]=indexer.search_by_BM25(query,k,b)[:20]
        query_id+=1
    
    query_id=1
    rel_BM25_3=defaultdict(list)   
    k=2.0
    b=0.5
    for query in query1:
        rel_BM25_3[query_id]=indexer.search_by_BM25(query,k,b)[:20]
        query_id+=1
    
    
    query_id=1
    rel_BM25_4=defaultdict(list)   
    k=2.0
    b=1.0
    for query in query1:
        rel_BM25_4[query_id]=indexer.search_by_BM25(query,k,b)[:20]
        query_id+=1
    
    """"for query_id in range(1,len(rel_cosine)+1):
        print query_id,
        print " ",
        for doc_id in rel_cosine[query_id]:
            print doc_id,
        print "\n" """
        
    
    
    rele=read_rel('time/TIME.REL')
    num_query=len(rele)
    print evaluation(rel_cosine,rele,num_query)
    print "Cosine               Precision= %.4f    Recall=%.4f    F1=%.4f    MAP=%.4f" %tuple((evaluation(rel_cosine,rele,num_query)))
    print "RSV                  Precision= %.4f    Recall=%.4f    F1=%.4f    MAP=%.4f" %tuple((evaluation(rel_RSV,rele,num_query)))
    print "BM25 (k=1,b=0.5)     Precision= %.4f    Recall=%.4f    F1=%.4f    MAP=%.4f" %tuple((evaluation(rel_BM25_1,rele,num_query)))
    print "BM25 (k=1,b=1)       Precision= %.4f    Recall=%.4f    F1=%.4f    MAP=%.4f" %tuple((evaluation(rel_BM25_2,rele,num_query)))
    print "BM25 (k=2,b=0.5)     Precision= %.4f    Recall=%.4f    F1=%.4f    MAP=%.4f" %tuple((evaluation(rel_BM25_3,rele,num_query)))
    print "BM25 (k=2,b=1)       Precision= %.4f    Recall=%.4f    F1=%.4f    MAP=%.4f" %tuple((evaluation(rel_BM25_4,rele,num_query)))
    curve(rel_RSV,rele,num_query)
       
        

if __name__ == '__main__':
    main()
