Edit this file and push to your private repository to provide answers to the following questions.

1. In `searcher.py`, why do we keep an inverted index instead of simply a list
of document vectors (e.g., dicts)? What is the difference in time and space
complexity between the two approaches?

    If we use a list of document vectors, we need to include the union of all terms of all documents in every single
    document vectors and therefore the space complexity is 2T * N, where T is the total number of terms in all the
    documents, and N is the number of documents. The reason to multiply TN with 2 is that we need to store the tf-idf
    weight for each term in each document. So if we use a list of document vectors, we waste a lot of space on storing
    those terms that don't appear in the documents. On the other hand, if we keep an inverted index, the space complexity
    will be 2t(1)+2t(2)+2t(3)+...+2t(N), where t(i) is the number of terms in ith document. By keeping an inverted index, 
    we save a lot of space. For time complexity, the runtime of an inverted index is O(Qn), where Q is number of query terms
    and n is number of documents containing each query term. However, the runtime of a list of document vectors is O(QN), 
    where Q is number of query terms and N is number of all documents. So by using an inverted index we also save time as well
    as space.   
    
    
2. Consider the query `chinese` with and without using champion lists.  Why is
the top result without champion lists absent from the list that uses champion
lists? How can you alter the algorithm to fix this?

    The reason may be that the top result document does not rank as the top 10 documents where the word 'chinese' appear most
    times in. Neither does the top result document rank as the top 10 documents where the word 'american' appear most times in.
    So the top result document is excluded from both champion lists of the query terms. However the document 5367 contains many
    'chinese' and 'american' since it rank as the top result. So it shows that the champion list of 'chinese' may not contain many
    'american'. And the champion list of 'american' may not contain many 'chinese'. Therefore we only consider the union of the two
    champion lists and exclude the document that is high in 'chinese american'. We can alter the algorithm by use larger threshold 
    of champion lists (e.g. threshold=50) and then take the intersection of the champion lists instead of taking the union. Then we
    use the intersection of the champion lists as the final champion list.

    
3. Describe in detail the data structures you would use to implement the
Cluster Pruning approach, as well as how you would use them at query time.

    I would use dictionary to implement the Cluster Pruning approach. I will store the leaders as the keys of the dictionary and 
    the value of each key will be its followers. At query time, I will compute the cosine similarities from query to each of the
    leaders and find the leader L (or leaders) that is closest to query. Then I will know which documents are the followers by using the key,
    which is the leader L (or leaders). Then I will iterate through the followers and compute the cosine scores for all followers of that
    leader (or leaders). Then I will rank the cosine scores.
 
    
