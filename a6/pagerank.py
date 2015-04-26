""" Assignment 6: PageRank. """

from collections import defaultdict
import glob
import urllib
import os

from BeautifulSoup import BeautifulSoup


def parse(folder, inlinks, outlinks):
    """
    Read all .html files in the specified folder. Populate the two
    dictionaries inlinks and outlinks. inlinks maps a url to its set of
    backlinks. outlinks maps a url to its set of forward links.
    """
    for url in glob.glob("%s/*.html" %(folder)):
        soup = BeautifulSoup(urllib.urlopen(url))
        links=set(["%s/%s" %(folder,a['href']) for a in soup.findAll('a') if a.get('href')])
        url="%s/%s" %(folder,os.path.basename(url))
        outlinks[url]=links
        for link in links:
            inlinks[link].add(url)


def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = 1-b + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0
    """
    len_outlinks=defaultdict(lambda:0)
    for u in outlinks:
        len_outlinks[u]=len(outlinks[u])
    rank=defaultdict(lambda:1.0)
    for i in range(iters):
        for u in urls:
            sum=0
            for link in inlinks[u]:
                sum+=1.0*rank[link]/len_outlinks[link]
            rank[u]=1-b+1.0*b*sum
    return rank


def run(folder, b):
    """ Do not modify this function. """
    inlinks = defaultdict(lambda: set())
    outlinks = defaultdict(lambda: set())
    parse(folder, inlinks, outlinks)
    urls = sorted(set(inlinks) | set(outlinks))
    ranks = compute_pagerank(urls, inlinks, outlinks, b=b)
    print 'Result for', folder, '\n', '\n'.join('%s\t%.3f' % (url, ranks[url]) for url in sorted(ranks))


def main():
    """ Do not modify this function. """
    run('set1', b=.5)
    run('set2', b=.85)


if __name__ == '__main__':
    main()
