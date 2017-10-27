import scrapy


class BiorxivSpider(scrapy.Spider):
    name = "biorxiv"

    def start_requests(self):
        urls = [
            'https://www.biorxiv.org/content/early/recent'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def getInfo(self, response):
        yield {
            "title": response.css(".highwire-cite-title::text").extract_first(),
            "authors": self.processAuthors(response),
            "doi": response.css(".highwire-cite-metadata-doi::text").extract_first(),
            "abstract": response.css(".highwire-markup .abstract #p-2::text").extract_first(),
            "link": response.css(".pane-biorxiv-art-tools .panel-region-content-left .inside .pane-custom a::attr(href)").extract_first(),
            "date": response.css(".pane-biorxiv-publication-history .published span::text").extract_first() + response.css(".pane-biorxiv-publication-history .published::text").extract_first()
        }

    def processAuthors(self, response):
        author_list = []
        for author in response.css(".main-content-wrapper .highwire-citation-author"):
            author_name = author.css(".nlm-given-names::text").extract_first()
            author_lastname = author.css(".nlm-surname::text").extract_first()
            author_list.append(author_name + " " + author_lastname)
        return author_list

    def parse(self, response):
        for link in response.css("span.highwire-cite-title"):
            inner_info = link.css("a::attr(href)").extract_first()
            if inner_info is not None:
                inner_info = response.urljoin(inner_info)
                yield scrapy.Request(inner_info, callback=self.getInfo)

        # next_page = response.css(".pager-wrapper .page-group-last .pager-next a::attr(href)").extract_first()

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        #tweets no se puede porque son generados dinamicamente por un widget y el scraping solo lee el html, no lee el contenido dinamico