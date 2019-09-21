from abc import ABC

import spacy
from bs4 import BeautifulSoup
from spacy.tokens.span import Span


class WordProcessing():

    def __init__(self,soup, languaje,regex):
        if languaje == "en":
            self.nlp = spacy.load("en_core_web_sm")
        elif languaje == "es":
            self.nlp = spacy.load("es_core_news_sm")
        else:
            self.nlp = spacy.load("en_core_web_sm")
        self.soup = soup
        self.regex = regex

    def wordProcessing(self):
        pass

    def create_tag(self,name_tag, dic, text):
        new_tag = self.soup.new_tag(name_tag)
        new_tag.attrs = dic
        new_tag.string = text
        return new_tag


def get_wikipedia_url(span):
    if span.label_ in ("PERSON", "ORG", "GPE", "LOCATION"):
        entity_text = span.text.replace(" ", "_")
        return "https://en.wikipedia.org/w/index.php?search=" + entity_text


class EntitiesProcessing(WordProcessing):
    def wordProcessing(self):
        switcher_color ={
            "PERSON":"#FF5733",
            "ORG":"#12DFE1",
            "GPE":"#1256E1",
            "LOCATION":"#8012E1"
        }
        Span.set_extension("wikipedia_url", getter=get_wikipedia_url)
        for heading in self.soup.find_all(self.regex):

            with self.nlp.disable_pipes('tagger','parser'):
                doc = self.nlp(heading.text)

            new_tag = self.soup.new_tag(heading.name)
            new_tag.attrs = heading.attrs
            for token,ent in zip(doc,doc.ents):
                if (token in ent) and ent._.wikipedia_url != None:
                    tag_font = self.create_tag(
                        "mark",
                        {"class": "entity",
                         "style": "background: "+ switcher_color[ent.label_] +"; line-height: 1;"
                                  " border-radius: 0.35em; box-decoration-break: clone;"
                                  " -webkit-box-decoration-break: clone"
                         },
                        ent.text + " "
                    )
                    tag_font.append(self.create_tag(
                        "a",
                        {"style": "font-size: 0.8em; font-weight: bold; "
                                  "line-height: 1; border-radius: 0.35em;"
                                  " text-transform: uppercase; vertical-align: middle; ",
                         "href":ent._.wikipedia_url,
                         "target":"_blank"},
                        ent.label_
                    ))
                    new_tag.append(tag_font)
                else:
                    new_tag.append(token.text + " ")
            heading.replace_with(new_tag)





class SemanticsProcessing(WordProcessing):
    def wordProcessing(self):
        for heading in self.soup.find_all(self.regex):

            with self.nlp.disable_pipes('parser', 'ner'):
                doc = self.nlp(heading.text)

            new_tag = self.soup.new_tag(heading.name)
            new_tag.attrs = heading.attrs
            for token in doc:
                if token.pos_ == "NOUN":
                    tag_font = self.create_tag(
                        "mark",
                        {"class": "entity",
                         "style": "background: #7aecec; line-height: 1;"
                                  " border-radius: 0.35em; box-decoration-break: clone;"
                                  " -webkit-box-decoration-break: clone"
                         },
                        token.text + " "
                    )
                    tag_font.append(self.create_tag(
                        "span",
                        {"style": "font-size: 0.5em; font-weight: bold; "
                                  "line-height: 1; border-radius: 0.35em;"
                                  " text-transform: uppercase; vertical-align: middle; "},
                        "Noun "
                    ))
                    new_tag.append(tag_font)
                elif token.pos_ == "PROPN":
                    tag_font = self.create_tag(
                        "mark",
                        {"class": "entity",
                         "style": "background: #feca74; line-height: 1;"
                                  " border-radius: 0.35em; box-decoration-break: clone;"
                                  " -webkit-box-decoration-break: clone"
                         },
                        token.text + " "
                    )
                    tag_font.append(self.create_tag(
                        "span",
                        {"style": "font-size: 0.5em; font-weight: bold; "
                                  "line-height: 1; border-radius: 0.35em;"
                                  " text-transform: uppercase; vertical-align: middle; "},
                        "Name "
                    ))
                    new_tag.append(tag_font)
                else:
                    new_tag.append(token.text + " ")
            heading.replace_with(new_tag)
