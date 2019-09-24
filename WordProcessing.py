import re
from abc import ABC

import spacy
from bs4 import BeautifulSoup
from spacy.tokens import Span,Token

from utils import switcher_color_entities,switcher_color_semantics


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
        Token.set_extension("wikipedia_url",getter=get_wikipedia_url_semantics)
        Span.set_extension("wikipedia_url", getter=get_wikipedia_url_entities)


    def wordProcessing(self):
        pass

    def create_tag(self,name_tag, dic, text):
        new_tag = self.soup.new_tag(name_tag)
        new_tag.attrs = dic
        new_tag.string = text
        return new_tag


def get_wikipedia_url_entities(span):
    if span.label_ in ("PERSON", "ORG", "GPE", "LOCATION"):
        entity_text = span.text.replace(" ", "_")
        return "https://en.wikipedia.org/w/index.php?search=" + entity_text

def get_wikipedia_url_semantics(token):
        return "https://en.wikipedia.org/w/index.php?search=" + token.text


class EntitiesProcessing(WordProcessing):
    def wordProcessing(self):
        for tag in self.soup.find_all(self.regex):

            with self.nlp.disable_pipes('tagger','parser'):
                doc = self.nlp(tag.text)

            new_tag = self.soup.new_tag(tag.name)
            new_tag.attrs = tag.attrs
            entities = { ent.start_char:ent for ent in doc.ents}
            tokens = [token.text for token in doc]
            jump = -1
            s = ""
            for index,char_s in enumerate(tag.text):
                if index<=jump:
                    continue

                if len(entities) != 0 and index in entities.keys():
                    ent = entities[index]
                    if ent._.wikipedia_url != None:
                        tag_font = self.create_tag(
                            "mark",
                            {"class": "entity",
                             "style": "background: "+ switcher_color_entities[ent.label_] +"; line-height: 1;"
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
                        new_tag.append(ent.text)
                    jump = ent.end_char
                    s = ""
                else:
                    s += char_s
                    if s.strip() in tokens:
                        new_tag.append(s)
                        s = ""
            tag.replace_with(new_tag)

class SemanticsProcessing(WordProcessing):
    def wordProcessing(self):
        for tag in self.soup.find_all(self.regex):

            with self.nlp.disable_pipes('parser', 'ner'):
                doc = self.nlp(tag.text)

            new_tag = self.soup.new_tag(tag.name)
            new_tag.attrs = tag.attrs
            for token in doc:
                if token.pos_ in switcher_color_semantics.keys():
                    tag_font = self.create_tag(
                        "mark",
                        {"class": "entity",
                         "style": "background: "+ switcher_color_semantics[token.pos_] +"; line-height: 1;"
                                  " border-radius: 0.35em; box-decoration-break: clone;"
                                  " -webkit-box-decoration-break: clone"
                         },
                        token.text + " "
                    )
                    tag_font.append(self.create_tag(
                        "a",
                        {"style": "font-size: 0.5em; font-weight: bold; "
                                  "line-height: 1; border-radius: 0.35em;"
                                  " text-transform: uppercase; vertical-align: middle; ",
                         "href": token._.wikipedia_url,
                         "target": "_blank"
                         },
                        token.pos_
                    ))
                    new_tag.append(tag_font)
                else:
                    new_tag.append(token.text + " ")
            tag.replace_with(new_tag)
