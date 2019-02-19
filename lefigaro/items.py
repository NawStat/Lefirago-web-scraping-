# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LefigaroItem(scrapy.Item):
    
    # define the fields for your item here like:
    Tel_agence = scrapy.Field()
    url = scrapy.Field()
    Price = scrapy.Field()
    Titre_annonce = scrapy.Field()
    Ville = scrapy.Field()
    Pays = scrapy.Field()
    m2_total= scrapy.Field()
    Non_agence = scrapy.Field()
    Adress_agence = scrapy.Field()
    CodePostal_agence = scrapy.Field()