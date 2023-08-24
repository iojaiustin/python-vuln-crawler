import crawler
import argparse
import sys
import xss

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("wordlist")
parser.add_argument("-v", "--verbose", help="Increase output verbosity",
                    action="store_true")
args = parser.parse_args()

verbose = args.verbose
url = args.url
wordlist = open(args.wordlist,"r")

def run(url,wordlist):
    for url in crawler.crawl(url):
        if verbose:
            print("[i] Testing ",url)
        xss.scan(url,wordlist)

run(url,wordlist)