import sys

from crawler import Crawler

if __name__ == '__main__':
    args = sys.argv
    arg_len = len(args)
    board = args[1]

    crawler = Crawler(board)
    crawler.crawl_pages()

    

                