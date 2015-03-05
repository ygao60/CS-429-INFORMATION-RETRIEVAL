""" Assignment 1

You will modify Assignment 0 to support phrase queries instead of AND queries.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Assume all multi-word queries are phrase queries. E.g., the query "why did
the" should be processed as a phrase, not a conjunction.

In addition, you will modify the tokenize method to keep hyphens and
apostrophes inside words, as well as add a stem method to collapse the terms
"did" and "does" to "do."  (More details are in the comments of each method.)

Finally, complete the find_top_bigrams method to find the most frequent
bigrams of (normalized) terms in the document set.

"""
from collections import defaultdict
import re


def read_lines(filename):
    """ Read a file to a list of strings. You should not need to modify
    this. """
    return [l.strip() for l in open(filename, 'rt').readlines()]


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Retain hyphens and apostrophes inside words. Remove all other
    punctuation and convert to lowercase.

    >>> tokenize("Hi there. What's going on? first-class")
    ['hi', 'there', "what's", 'going', 'on', 'first-class']
    """
    return re.findall("\w+(?:[-']\w+)*",document.lower())


def stem(tokens):
    """
    Given a list of tokens, collapse 'did' and 'does' into the term 'do'.

    >>> stem(['did', 'does', 'do', "doesn't", 'splendid'])
    ['do', 'do', 'do', "doesn't", 'splendid']
    """
    for i in range(len(tokens)):
		if tokens[i]=='did' or tokens[i]=='does':
			tokens[i]='do'
    return tokens


def create_positional_index(tokens):
    """
    Create a positional index given a list of normalized document tokens. Each
    word is mapped to a list of lists (using a defaultdict). Each sublist
    contains [doc_id position_1 position_2 ...] -- this indicates the document
    the word appears in, as well as the word offset of each occurrence.

    >>> index = create_positional_index([['a', 'b', 'a'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [[0, 0, 2], [1, 0]]
    >>> index['b']
    [[0, 1]]
    >>> index[('c')]
    [[1, 1]]
    """
    d=defaultdict(list)
    docid=0
    len={}
    for doc in tokens:
        for word in doc:
            if word not in len.keys():
                len[word]=0
            
    for doc in tokens:
        pos=0
        appear=[]
        for word in doc:
            if word not in appear:
                d[word].append([docid, pos])
                len[word]=len[word]+1
                appear.append(word)
            else:
                d[word][len[word]-1].append(pos)
            pos=pos+1
        docid=docid+1
    return d


def phrase_intersect(list1, list2):
    """ Return the intersection of two positional posting lists. A match
    requires a position in list1 to be one less than a position in list2 in
    the same document.

    Your implementation should be linear in the length of the number of
    positions in each list. That is, you should access each position value at
    most once.

    In the example below, word1 occurs in document 0 (positions 1,4), document
    1 (position 0), and document 10 (positions 2, 3, 4). Word2 occurs in
    document 0 (positions 2, 6), document 1 (position 2), document 2 (position
    0), and document 10 (position 1, 5). Thus, the phrase "word1 word2" occurs
    in document 0 (position 1->2) and in document 10 (position 4->5).

    >>> phrase_intersect([[0, 1, 4], [1, 0], [10, 2, 3, 4]], \
                         [[0, 2, 6], [1, 2], [2, 0], [10, 1, 5]])
    [[0, 2], [10, 5]]
    >>> phrase_intersect([[1, 2]], [[1, 4]])
    []
    """
    i=0
    j=0
    list3=[]
    len3=0
    while i<len(list1) and j<len(list2):
        if(list1[i][0]==list2[j][0]):
            p1=1
            p2=1
            appear=False
            docid=list1[i][0]
            while p1<len(list1[i]) and p2<len(list2[j]):
                if list2[j][p2]==list1[i][p1]+1:
                    if appear==False:
                        list3.append([docid, list2[j][p2]])
                        len3=len3+1
                        appear=True
                    else:
                        list3[len3-1].append(list2[j][p2])
                    p1=p1+1
                    p2=p2+1
                elif list2[j][p2]<list1[i][p1]+1:
                    p2=p2+1
                else:
                    p1=p1+1
            i=i+1
            j=j+1
        elif (list1[i][0]<list2[j][0]):
            i=i+1
        else:
            j=j+1
    return list3
    


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that
    query is a single string, possible containing multiple words. Assume
    queries with multiple words are phrase queries. The steps are to:

    1. Tokenize the query
    2. Stem the query tokens
    3. Intersect the positional postings lists of each word in the query, by
    calling phrase_intersect.

    E.g., below we search for documents containing the phrase 'a b':
    >>> search({'a': [[0, 4], [1, 1]], 'b': [[0, 5], [1, 10]], 'c': [[0, 6], [1, 11]]}, 'a b')
    [0]
    """
    term=stem(tokenize(query))
    l=len(term)
    for i in term:
        if i not in index.keys():
            doc=[]
            break
    else:
        if l==1:
                doc=index[term[0]]
        else:
            doc=phrase_intersect(index[term[0]],index[term[1]])
            if l>2:
                for i in range(2,l):
                    doc=phrase_intersect(doc, index[term[i]])
    docid=[]
    if len(doc)>0:
        for list in doc:
            docid.append(list[0])
    return docid
        

def find_top_bigrams(terms, n):
    """
    Given a list of lists containing terms, return the most frequent
    bigrams. The return value should be a list of tuples in the form (bigram,
    count), in descending order, limited to the top n bigrams. In the example
    below, there are two documents provided; the top two bigrams are 'b c' (3
    occurrences) and 'a b' (2 occurrences).

    >>> find_top_bigrams([['a', 'b', 'c', 'd'], ['b', 'c', 'a', 'b', 'c']], 2)
    [('b c', 3), ('a b', 2)]
    """
    d={}
    for i in terms:
        l=len(i)
        for j in range(l-1):
            seq=" ".join([i[j], i[j+1]])
            if seq in d.keys():
                d[seq]=d[seq]+1
            else:
                d[seq]=1
    list=d.items()
    sort=sorted(list, key=lambda x:x[1], reverse=True)
    return sort[:n]
    
    


def main():
    """ Main method. You should not modify this. """
    documents = read_lines('documents.txt')
    terms = [stem(tokenize(d)) for d in documents]
    index = create_positional_index(terms)
    queries = read_lines('queries.txt')
    for query in queries:
        results = search(index, query)
        print '\n\nQUERY:', query, '\nRESULTS:\n', '\n'.join(documents[r] for r in results)

    print '\n\nTOP 11 BIGRAMS'
    print '\n'.join(['%s=%d' % (bigram, count) for bigram, count in find_top_bigrams(terms, 11)])


if __name__ == '__main__':
    main()
