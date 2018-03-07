import urllib.request
import os
import re

filter = ['img', 'favicon', 'ico']

def get_url_html(url):
    """
        Gets the html of the url specified and returns it as a string

        Arguments:
            url (:class:`str`): The url of the page to grab

        Returns:
            (:class:`str`): The html of the url as a string
    """
    print("grabbing html for {}".format(url))
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    return mystr

def get_all_links(html):
    """
        Gets all of the links in the html and retuns them

        Arguments:
           html  (:class:`str`): The html of the page

        Returns:
            (:class:`list`): A list of all of the links on the page
    """
    links = []
    lines = html.split('\n')
    anchor_regex = re.compile(r"href=\"([^\"]+)\"")
    for line in lines:
        match = re.search(anchor_regex, line)
        if match:
            links.append(match.groups()[0])
    return links 

def filter_links(base_url, links, filter):
    ret_links = []
    for link in links:
        if base_url in link:
            valid = True
            for filt in filter:
                if filt in link:
                    valid = False 
                    break
            if valid:
                ret_links.append(link)
    return ret_links

def get_new_links(links, visited):
    """
        Goes through links and finds all that aren't in visited and 
        returns them

        Arguments:
           links (:class:`list`): New links
           visited (:class:`list`): Links we've visited

        Returns:
            (:class:`list`): List of all links not in visited
    """
    new_links = []
    for link in links:
        if link not in visited:
            new_links.append(link)
    return new_links

def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def create_html_file(url, html, directory_name):
    os.system("echo {} > {}/{}".format(html, directory_name, url))

def scrape(url, visited_urls, directory_name, base_url):
    html = get_url_html(url)
    create_html_file(url, html, directory_name)

    links = get_all_links(html)
    links = filter_links(base_url, links, filter)

    new_links = get_new_links(links, visited_urls)
    links += new_links
    for link in new_links:
        scrape(link, links, directory_name, base_url)

def start_scrape(base_url, visited_urls):
    directory_name = re.search(re.compile(r"([a-z]+\.[a-z]+)/"), 
                               base_url).groups()[0]
    create_directory(directory_name)
    scrape(base_url, visited_urls, directory_name, directory_name)

