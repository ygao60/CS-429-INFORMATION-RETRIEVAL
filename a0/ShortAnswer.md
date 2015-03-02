Edit this file in your private repository to provide answers to the following questions (from MRS).

1. Extend the postings merge algorithm to arbitrary Boolean query formulas. What is
its time complexity? For instance, consider:

  `(Brutus OR Caesar) AND NOT (Antony OR Cleopatra)`

  Can we always merge in linear time? Linear in what? Can we do better than this?

  We can always merge in linear time. The intersection time is O(qN) where q is the number of query terms and N is the number
  of documents. We cannot do better than this.

  
2. If the query is:

  `friends AND romans AND (NOT countrymen)`

  How could we use the frequency of countrymen in evaluating the best query evaluation order? In particular, propose a way of handling negation in determining the order of query processing.
  
  If the negated term is frequent, use N-(length of postings list) to determine the order of processing in place of (length of postings list). And create a new posting list for 
  the negated term, which is all documents minus the postings list of the negated term. Then use this new postings list to intersect with other terms' postings list.
  If the negated term is infrequent, use the (length of postings list) to determine the order of processing. And when it comes to the intersection of the  negated term's posting list, 
  delete document id from the merging postings list if that document id appears in both the merging postings list and the negated term's posting list.
  
  
3. For a conjunctive query, is processing postings lists in order of size guaranteed to be
optimal? Explain why it is, or give an example where it isn’t.

  Processing postings lists in order of size is not guaranteed to be optimal. For example, if there are three terms with postings list size l1=15, l2=30, l3=80. If the intersection of l1 and l2
  has a size of 10 and the intersection of l1 and l3 has a size of 1. Then the order of l1, l2, l3 will have 15+30+10+80=135 steps when intersecting. The order of l1, l3, l2 will have 15+80+1+30=126 steps
  when intersecting, which requires less steps. 
