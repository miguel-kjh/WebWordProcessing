import webbrowser

from bs4 import BeautifulSoup
import requests

from WordProcessing import SemanticsProcessing,EntitiesProcessing


class WebWordProcessing:
    def __init__(self, url, html_parser="lxml"):
        req = requests.get(url)
        self.soup = BeautifulSoup(req.text, html_parser)
        try:
            self.languaje = self.soup.html.attrs['lang']
        except:
            self.languaje = None

    def getSoup(self): return self.soup

    def getLanguaje(self): return self.languaje

    def saveHtml(self):
        with open("example_modified.html", "wb") as f_output:
            f_output.write(self.soup.prettify("utf-8"))

    def viewHtml(self):
        webbrowser.open("example_modified.html")

    def processing(self, regex, type="Semantics"):
        if type == "Semantics":
            wp = SemanticsProcessing(self.soup,self.languaje,regex)
        elif type == "Entities":
            wp = EntitiesProcessing(self.soup,self.languaje,regex)
        else: return None
        wp.wordProcessing()


