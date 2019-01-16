"""
# @auther: t-peshi@microsoft.com
# @time: 12/21/2018
# @file: {wiki_multi_languages}.py

"""
import re
import requests
from bs4 import BeautifulSoup


class WikiMultiLanguages(object):
    def __init__(self):
        self.info = "crawler of wiki-pedia"
        self.start_url = "https://www.wikipedia.org/"
        self.url_set = set()
        self.parsed_url = set()
        self.text_collector = []

    def get_texts_pipline(self):
        self.collect_urls()
        # TODO: parallel processing
        for page_url in self.url_set:
            page_text = self.get_page_key_words(page_url)
            self.text_collector.append(page_text)
        return self.text_collector

    def collect_urls(self):
        """
        root function
        :return:
        """
        country_homepages = self.get_language_homepage()
        # TODO: parallel processing
        for homepage in country_homepages:
            self.parse_page_bfs(home_url=homepage, page_url=homepage)
            # return self.text_collector

    def get_language_homepage(self):
        """
        :return: 61 languages home page url
        """
        main_page = requests.get(self.start_url)
        soup = BeautifulSoup(main_page.content, "html.parser", from_encoding="utf-8")
        country_html = soup.find_all("div", class_="hide-arrow")
        country_html = country_html[0].find_all('option')
        country_lst = [str(ch['lang']) for ch in country_html]
        country_page = ["https://" + cl + ".wikipedia.org/" for cl in country_lst]
        return country_page

    def parse_page_bfs(self, home_url, page_url):
        """
        the
        :param home_url:
        :param page_url:
        :return: recursive method, text_collector will collect page sentences each loop
        """
        # page_text = self.get_page_key_words(page_url)
        # self.text_collector.append(page_text)
        # TEST CONDITION
        if len(self.url_set) > 100:
            return
        urls = self.get_page_urls(home_url=home_url, page_url=page_url)
        # TODO: parallel processing here
        for url in urls:
            self.url_set.add(str(url))
            self.parse_page_bfs(home_url=home_url, page_url=url)

    def get_page_key_words(self, page_url):
        """
        :param page_url:
        :return: open a page and download all key words with hyperlink
        """
        print("=============load page:{}===============".format(page_url))
        page_html = requests.get(page_url)
        soup = BeautifulSoup(page_html.content)
        text_key_html = soup.find_all("a")
        text = [tkh.text for tkh in text_key_html]
        return text

    def get_page_urls(self, page_url, home_url):
        """

        :param page_url: the url of one page
        :param home_url: the wiki-pedia home page of one specific language
        :return: all key word urls of this page
        """
        # page_url = "https://zh.wikipedia.org/wiki/%E9%87%8D%E5%AD%90%E5%88%97%E8%A1%A8"
        page_html = requests.get(page_url)
        soup = BeautifulSoup(page_html.content)
        text_html = soup.find_all("a")
        urls = []
        for a in text_html:
            try:
                urls.append(a['href'])
                if len(urls) % 100 == 0:
                    print(" ---add 1000 urls---")
            except:
                print("no link")
        urls = [home_url + u if u.find('http') == -1 else u for u in urls]

        return urls

    def clean_text(self, text):
        return text

    def get_full_page(self, soup_file):
        text = soup_file.get_text()
        return text


if __name__ == "__main__":
    wiki = WikiMultiLanguages()
    # res = wiki.get_language_homepage()
    res = wiki.get_texts_pipline()
