"""
Assignment 4. Implement a Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

import glob
from collections import defaultdict
import math


class Document(object):
    """ A Document. DO NOT MODIFY.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename):
        self.filename = filename
        self.label = 'spam' if 'spmsg' in filename else 'ham'
        self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):

    def train(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your book.
        """
        N=len(documents)
        C=[0,1]
        prior=[0,0]
        Nc=[0,0]
        Tct0=defaultdict(lambda:0)
        Tct1=defaultdict(lambda:0)
        Tct=[Tct0,Tct1]
        l=[0,0]
        V=set()
        condprob0={}
        condprob1={}
        condprob=[condprob0,condprob1]
        
        for doc in documents:
            if(doc.label=='spam'):
                c=0
            else:
                c=1
            Nc[c]+=1
            for t in doc.tokens:
                Tct[c][t]+=1
            l[c]+=len(doc.tokens)
            V=V | set(doc.tokens)
            
        lenV=len(V)
        
        for c in C:
            prior[c]=1.*Nc[c]/N
            L=l[c]+lenV
            for t in V:
                condprob[c][t]=1.*(Tct[c][t]+1)/L
                
        self.V=V
        self.prior=prior
        self.condprob=condprob
            

    def classify(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Return a list of strings, either 'spam' or 'ham', for each document.
        documents....A list of Document objects to be classified.
        """
        
        V=self.V
        prior=self.prior
        condprob=self.condprob
        W=[]
        log_prior=[0,0]
        C=[0,1]
        score=[0,0]
        prediction=[]
        
        for c in C:
            log_prior[c]=math.log10(1.*prior[c])
        for doc in documents:
            W=[]
            for t in doc.tokens:
                if t in V:
                    W.append(t)
           
            for c in C:
                score[c]=log_prior[c]
                for t in W:
                    score[c]+=math.log10(1.*condprob[c][t])
            if score[0]>score[1]:
                prediction.append('spam')
            else:
                prediction.append('ham')
        return prediction


def evaluate(predictions, documents):
    """
    TODO: COMPLETE THIS METHOD.

    Evaluate the accuracy of a set of predictions.
    Print the following:
    accuracy=xxx, yyy false spam, zzz missed spam
    where
    xxx = percent of documents classified correctly
    yyy = number of ham documents incorrectly classified as spam
    zzz = number of spam documents incorrectly classified as ham

    See the provided log file for the expected output.

    predictions....list of document labels predicted by a classifier.
    documents......list of Document objects, with known labels.
    """
    i=0
    correct=0
    zzz=0
    yyy=0
    for doc in documents:
        label=doc.label
        if (label==predictions[i]):
            correct+=1
        else:
            if (label=='spam'):
                zzz+=1
            else:
                yyy+=1
        i+=1
    xxx=1.*correct/len(documents)
    print ('accuracy=%.3f, %d false spam, %d missed spam' %(xxx,yyy,zzz))
    

def main():
    """ DO NOT MODIFY. """
    train_docs = [Document(f) for f in glob.glob("train/*.txt")]
    print 'read', len(train_docs), 'training documents.'
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(f) for f in glob.glob("test/*.txt")]
    print 'read', len(test_docs), 'testing documents.'
    predictions = nb.classify(test_docs)
    evaluate(predictions, test_docs)

if __name__ == '__main__':
    main()
