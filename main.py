import re

from WebWordProcessing import WebWordProcessing
url ="https://code.tutsplus.com/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211"
url2 = "http://www.bbc.com/future/story/20190919-the-simple-words-that-save-lives"
if __name__ == '__main__':
    wwp = WebWordProcessing(url)
<<<<<<< HEAD
    wwp.processing(re.compile("p|h[1-6]"), type="Entities")
=======
    wwp.processing(re.compile("p|h[1-6]"))
>>>>>>> 05c1d48e0a182aefda5ea1b11533a042ea56c4be
    wwp.saveHtml()
    wwp.viewHtml()