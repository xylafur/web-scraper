import urllib.request
import os
import re

filter = ['img', 'favicon', 'ico', 'javascript']

def get_url_html(url):
    """
        Gets the html of the url specified and returns it as a string

        Arguments:
            url (:class:`str`): The url of the page to grab

        Returns:
            (:class:`str`): The html of the url as a string
    """
    if 'http://' not in url:
        url = 'http://' + url
    print("grabbing html for {}".format(url))
    try:
        fp = urllib.request.urlopen(url)
    except (urllib.error.HTTPError, urllib.error.URLError):
        return ""
    mybytes = fp.read()
    try:
        mystr = mybytes.decode("utf8")
    except UnicodeDecodeError:
        fp.close()
        return ""
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
    """
        Ensures that all of the links are a part of the original 
        website.  Also removes links that don't follow the filter

        Arguments:
            base_url (:class:`str`): THe name of the site we're 
                                     scraping.  THe name of the 
                                     direcctory we are saving all 
                                     of the sites in is what is 
                                     expected most likely

            links (:class:`list`): THe links we are filtering

            filter (:class:`list`): A list of strings that should 
                                    not be in any of the links

        Returns:    
            (:class:`list`): THe filtered link list
    """
    ret_links = []
    for link in links:
        if base_url in link:
            valid = True
        elif link[0] == '/':
            if base_url[-1] == '/' or link[0] == '/':
                link = base_url + link
            else:
                link = base_url + '/' + link
            valid = True
        if valid:
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
    """
        Checks if a directory exists and creates it
        
        Arguments:
           directory_name (:class:`str`): What to name the directory
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def create_html_file(url, html, directory_name):
    """
        Puts the html gatered as a string into a file 

        Arguments:
           url (:class:`str`):  The url of the page(what we will name 
                                the file)

           html (:class:`str`): The html of the page

           directory_name (:class:`str`): The name of the directory 
                                          we are putting the file in
    """
    if directory_name not in url:
        print("Did not find {} in url {}".format(directory_name, url))
        return
    #this regex is wrong, its only grabbing the base  website
    url = re.search(re.compile(r"/([a-z.]+[a-z]+)"), 
                               url).groups()[0]
    f = "{}/{}".format(directory_name, url) 
    os.system("touch {}".format(f))
    file = open(f, 'w')
    file.write(html)
    file.close()
    print("created file {}".format(f))

def scrape(url, visited_urls, directory_name, base_url):
    """
        Recursive function.
        Grabs the html of the provided url and createes a file for 
        it.  Grabs all links on the page and filters them.  Calls the 
        function on all valid links that have not yet been visited.

        Arguments:
           url (:class:`str`):  The url of the page(what we will name 
                                the file)

           visited_urls (:class:`list`): All of the pages we have 
                                         visited

           directory_name (:class:`str`): The name of the to put 
                                          files 

           base_url (:class:`str`): The website we are scraping
    """
    html = get_url_html(url)
    if not html:
        print("Was not able to get file for {}".format(url))
        return

    create_html_file(url, html, directory_name)

    links = get_all_links(html)
    links = filter_links(base_url, links, filter)

    new_links = get_new_links(links, visited_urls)
    links += new_links

    #have to identify that it is indeed a url

    for link in new_links:
        scrape(link, links, directory_name, base_url)

def start_scrape(base_url):
    """
        Scraping starting point.  Creates the directory that will 
                                  hold our files and then calls the 
                                  recursive function
        Arguments:
           base_url (:class:`str`): The website we are scraping
    """
    print("Scraping website: {}".format(base_url))

    directory_name = re.search(re.compile(r"([a-z.]+[a-z]+)/"), 
                               base_url).groups()[0]
    visited_urls = [base_url]
    print("Site will be located in {}".format(directory_name))
    create_directory(directory_name)
    scrape(base_url, visited_urls, directory_name, directory_name)
    print("Finished scraping site")

