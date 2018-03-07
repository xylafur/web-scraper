import sys

from scraper import start_scrape

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("This program requires a single input, the url of the"
              " main site to scrape")
        exit(1)
    base = sys.argv[1]

    url_list = [base]

    start_scrape(base, url_list)

