import re

from WebWordProcessing import WebWordProcessing
url ="https://code.tutsplus.com/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211"
url2 = "https://www.bbc.com/news"
if __name__ == '__main__':
    wwp = WebWordProcessing(url)
    wwp.processing(re.compile("p|h[1-6]"))
    wwp.saveHtml()
    wwp.viewHtml()