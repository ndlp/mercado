# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
	name = 'mercado'
	item_count = 0
	allowed_domain = ['https://www.mercadolibre.com.pe/']
	start_urls = ['https://listado.mercadolibre.com.pe/impresoras#D[A:impresoras]']

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="pagination__next"]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//*[@class="item__title list-view-item-title" ]')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		ml_item = MercadoItem()
		#info de producto
		ml_item['titulo'] = response.xpath('normalize-space(//*[@class="item-title__primary"]/text())').extract_first()
		ml_item['folio'] = response.xpath('normalize-space(//*[@class="item-info__id-number"]/text())').extract()
		ml_item['precio'] = response.xpath('normalize-space(//span[@class="price-tag-fraction"]/text())').extract()
		ml_item['envio'] = response.xpath('normalize-space(//*[@class="shipping-method-title"]/text())').extract()
		ml_item['ubicacion'] = response.xpath('normalize-space(//*[@class="custom-address"]//text())').extract()
		ml_item['ventas_producto'] = response.xpath('normalize-space(//*[@class="item-conditions"]/text())').extract()

		#info de la tienda o vendedor
		ml_item['vendedor_url'] = response.xpath('//*[@class="reputation-view-more card-block-link"]/@href').extract()
		ml_item['ventas_vendedor'] = response.xpath('normalize-space(//*[@class="reputation-relevant"][2]/strong').extract()
		ml_item['reputacion'] = response.xpath('normalize-space(//*[@class="reputation-relevant"][1]/strong').extract()

		self.item_count += 1
		if self.item_count > 5:
			raise CloseSpider('item_exceeded')
		yield ml_item
