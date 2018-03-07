import sys

from scraper import start_scrape

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("This program requires a single input, the url of the"
              " main site to scrape")
        exit(1)
    if 'http://' not in sys.argv[1]:
        print("The full url is required!")
        print("Ex: http://website_name.extention/")
        exit(1)

    base = sys.argv[1]

    if base[-1] != '/':
        base += '/'

    start_scrape(base)

