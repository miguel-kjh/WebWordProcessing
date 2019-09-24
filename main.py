import re

from WebWordProcessing import WebWordProcessing
url ="https://code.tutsplus.com/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211"
url2 = "http://www.bbc.com/future/story/20190919-the-simple-words-that-save-lives"
if __name__ == '__main__':
    wwp = WebWordProcessing(url)
    wwp.processing(re.compile("h[1-6]"), type="Entities")
    wwp.saveHtml()
    wwp.viewHtml()