import scrapy


class AliSpider(scrapy.Spider):
    name = 'ali'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4891.124 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://qcrc.qef.org.hk/en/search/result.php?from=&to=&deliverid%5B%5D=1&gp0=rrc_aids_home&gp1=rrc_aids_home&web=this&tpl_id=rrc_aids&ui_charset=utf-8&ui_lang=zh-hk&proxyreload=1&query=&filter_submit=Search&page='
        for page in range(1, 186):
            yield scrapy.Request(url + str(page), callback=self.parse_page, headers=self.headers)

    def parse_page(self, response):
        for link in response.css('div.btn-01 a::attr(href)').getall():
            yield response.follow(link, callback=self.parse, headers=self.headers)

    def parse(self, response):
        data = response.css('div.col-lg-10')
        links = response.css('div.content a::attr(href)').getall()
        try:
            proposal = links[0]
        except:
            proposal = ''

        try:
            report = links[1]
        except:
            report = ''
        try:
            grantee = data[1].css('div a::text').get().replace('\t', '').replace('\n', '').replace('\r', '')
        except:
            grantee = data[1].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', '')


        yield {
            'Title': response.css('div h2::text').get().replace('\”', '').replace('"', ''),
            'Project Period': data[0].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Grantee': grantee,
            'Project Nature': data[2].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Category': data[3].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Sub-category': data[4].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Applicant sector': data[5].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Beneficiary': data[6].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Project no': data[7].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Grant approved': data[8].css('div::text').get().replace('\t', '').replace('\n', '').replace('\r', ''),
            'Proposal':  proposal,
            'Report': report
        }
