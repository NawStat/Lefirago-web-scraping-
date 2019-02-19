# -*- coding: utf-8 -*-
import scrapy
from lefigaro.items import LefigaroItem 
#import pdb
import re
import json

class LefigarospiderSpider(scrapy.Spider):
	name = 'lefigaro'
	allowed_domains = ['properties.lefigaro.com']
	start_urls = ['https://properties.lefigaro.com/announces/luxury-real+estate-properties+for+sale-world/']

	def parse(self, response):
		for href in response.xpath("//a[contains(@class,'itemlist js-itemlist')]//@href"):
			# add the scheme, eg http://
			url  = "https://properties.lefigaro.com" + href.extract() 
			yield scrapy.Request(url, callback=self.parse_dir_contents)
		next_page = response.xpath("//a[contains(@class,'wrap-pagination-item js-page-next')]//@href").extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)

	def parse_dir_contents(self, response):
		item=LefigaroItem()
		block=response.xpath("//span[@itemprop='name']/text()").extract() 	
		#Titre annonce 
		try : 
			item['Titre_annonce'] =block[4]
		except:  item['Titre_annonce']= ''
		#Ville
		local = response.xpath("//span[@itemprop='addressLocality']/text()").extract_first().strip()

		#country
		try:
			item['Pays'] =  local[local.find('(')+1 : local.find(')')]
		except: item['Pays'] = ''
		#ville
		try:
			item['Ville'] =  local.replace('('+item['Pays']+')','')
		except: item['Ville'] = ''
		#métre carrés
		try:
			item['m2_total'] =  response.xpath("//span[@class='nb']/text()").extract_first()
		except: item['m2_total'] = ''
		# Links  
		item['url'] = response.xpath("//meta[@property='og:url']/@content").extract_first()
		annonce_id=re.findall('\d+', item['url'])
		try:
			item['Price'] = response.xpath("//div[contains(@class,'prix-annonce')]/strong[@class='price']/text()").extract_first().strip()
		except:
			item['Price'] =  ''
		## agence contact
		# Nom d'agence
		try: 
			item['Non_agence'] =  response.xpath("//ul[@class='agency-detail']/li/p[@class='h2-like']/text()").extract_first()
		except: item['Non_agence'] = ''
		# adresse agence et code postal 	 
		try:
			adresse= response.xpath('//p[@class="agency-localisation"]/text()').extract_first().strip()
			item['Adress_agence'] =''.join(response.xpath('//p[@class="agency-localisation"]/text()').extract()).replace('\n',' ').replace('  ','')
		except: 
			item['Adress_agence'] = ''
		#code postal
		try:
			code_postal=re.findall('\d+',item['Adress_agence'])
			for i in code_postal:
				if ((len(str(i)))>3) : item['CodePostal_agence']=i  
		except:
			item['CodePostal_agence'] = ""
		#pdb.set_trace()
		#telephone 
		link="https://proprietes.lefigaro.fr/ws/tel_annonce/pdf/"+str(annonce_id[0])+'/'
		#pdb.set_trace()
		yield scrapy.Request(url=link, meta = {'item':item},callback=self.prase_telephone,dont_filter = True)

		##Pagination
	def  prase_telephone(self, response):
		item = response.meta['item']
		try:
			telJson = json.loads(response.body_as_unicode())
			#	pdb.set_trace() 
			item ["Tel_agence"] = telJson["tel"]
		except:
			item ["Tel_agence"]=''
		#pdb.set_trace()

		yield item
	
