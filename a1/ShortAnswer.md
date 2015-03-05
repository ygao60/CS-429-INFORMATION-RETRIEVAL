Edit this file in your private repository to provide answers to the following questions.

1. Consider merging the following two lists, where the first list has skip pointers.
![skips](skips.png)
  1. How often is a skip pointer followed (i.e., p1 is advanced to skip(p1))?

    The skip pointer is followed once. (from 24 to 75)

  2. How many postings comparisons will be made by this algorithm while intersecting the two lists?

    19 comparisons are made. The comparisons are: (3,3),(5,5),(9,89),(15,89),(24,89),(75,89),(75,89),(92,89),(81,89),
    (84,89),(89,89),(92,95),(115,95),(96,95),(96,97),(97,97),(100,99),(100,100),(115,101)    
  
  3. How many postings comparisons would be made if the postings lists are intersected without the use of skip pointers?
  
    19 comparisons are made. The comparisons are: (3,3),(5,5),(9,89),(15,89),(24,89),(39,89),(60,89),(68,89),(75,89),
    (81,89),(84,89),(89,89),(92,95),(96,95),(96,97),(97,97),(100,99),(100,100),(115,101) 
    

2. Compute the Levenshtein edit distance between *paris* and *alice*. Fill in the 5 × 5 table below of
distances between all preﬁxes as computed by the algorithm in Figure 3.5 in [MRS](http://nlp.stanford.edu/IR-book/pdf/03dict.pdf). Cell (*i*, *j*) should store the minimum edit distance between the first *i* characters of *alice* and the first *j* characters of *paris* (as in the bottom right number of each cell in Figure 3.6).

  |       |   | p | a | r | i | s |
  |-------|---|---|---|---|---|---|
  |       | 0 | 1 | 2 | 3 | 4 | 5 |
  | **a** | 1 | 1 | 1 | 2 | 3 | 4 |
  | **l** | 2 | 2 | 2 | 2 | 3 | 4 |
  | **i** | 3 | 3 | 3 | 3 | 2 | 3 |
  | **c** | 4 | 4 | 4 | 4 | 3 | 3 |
  | **e** | 5 | 5 | 5 | 5 | 4 | 4 |

3. (Inspired by [H Schütze](http://www.cis.uni-muenchen.de/~hs/teach/13s/ir/).)We define a *hapax legomenon* as a term that occurs exactly once in a collection. We want to estimate the number of hapax legomena using Heaps’ law and Zipf’s law.
    1. How many unique terms does a web collection of 400,000,000 web pages containing 400 tokens on average have? Use the Heaps parameters k = 100 and b = 0.5.
    2. Use Zipf’s law to estimate the proportion of the term vocabulary of the collection that consists of hapax legomena. You may want to use the approximation 1/1 + 1/2 + ... + 1/*n* = ln *n*
    3. Do you think that the estimate you get is correct? Why or why not?

    answer:
  (1).  V=k*(T^b)=100*((400,000,000*400)^0.5)=40,000,000  unique terms
  
  (2).  Zipf's Law: f=k/i
      The sum of all collection frequencies equals the total number of tokens:
      (400,000,000*400)=k/1+k/2+k/3+...+k/(40,000,000)=(approximation) k*ln(40,000,000)=k*17.5044 
      =>  k=(400,000,000*400)/17.5044= 9.14*(10^9)
      
      The frequency of the least frequent term (i=40,000,000) is:
      f= k/i= 9.14*(10^9)/40,000,000= 228.5
      The least frequency term appear about 228.5 times. 
      So there is no hapax legomenon in the collection.
      So the proportion of hapax legomenon is 0.
      
  (3).  The estimate is not correct. Normally the proportion of hapax legomenon should be about 50%.