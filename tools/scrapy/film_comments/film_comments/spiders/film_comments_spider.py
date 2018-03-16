# encoding=utf-8
from scrapy import Spider
from film_comments.items import FilmCommentsItem 
from scrapy.http import Request, FormRequest 

class DouBanSpider(Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    # the start page for all palying film now
    start_urls = ['https://movie.douban.com/cinema/nowplaying/nanjing/']
    headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Connection":"keep-alive",
            "User-Agent":"'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'"
        }

    def __init__(self, FILM_NAME=None, COOKIES="", *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.FILM_NAME = FILM_NAME
        self.COOKIES = {} 
        i = 0 
        COOKIES = COOKIES.split('@')
        while(i<len(COOKIES)-1):
            self.COOKIES[COOKIES[i]] = COOKIES[i+1]
            i += 2

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(url=start_url, 
                cookies = self.COOKIES,
                callback=self.parse_first_page)

    def parse_first_page(self, response):
        dic = {}
        for sel in response.xpath("//div[@id='nowplaying']//li[starts-with(@class, 'list-item')]"):
            infoLst = sel.xpath("@id|@data-title").extract()
            if(len(infoLst)>0):
                dic[infoLst[1]] = infoLst[0]
                self.logger.info("Name:{}\tId:{}".format(infoLst[1], infoLst[0]))
        if(len(dic) > 0):
            if(not self.FILM_NAME.lower() == 'all'):
                try:
                    yield Request(url="https://movie.douban.com/subject/" + dic[self.FILM_NAME] + "/comments", 
                            cookies = self.COOKIES,
                            callback=self.parse)
                except KeyError as e:
                    self.logger.error("这部电影不再上映之列：{}".format(self.FILM_NAME))
                    return
                except Exception as e:
                    self.logger.error("发生错误：{}".format(e.args[0]))
                    return
            else:
                for info in dic.values():
                    yield Request(url="https://movie.douban.com/subject/" + info + "/comments", 
                            cookies = self.COOKIES,
                            callback=self.parse)
        else:
            yield response.request 

    def parse(self, response):
        filmName = ''.join(response.xpath("//div[@id='content']/h1/text()").extract()).split(' ')
        print(filmName)
        if(len(filmName) > 1):
            filmName.pop()
        for sel in response.xpath("//div[@class='comment-item']/div[@class='comment']"):
            comment = FilmCommentsItem()
            comment['cus_name'] = sel.xpath(".//span[@class='comment-info']/a/text()").extract()
            comment['comment'] = sel.xpath("p/text()").extract()
            comment['grade'] = sel.xpath(".//span[@class='comment-info']/span[@class[contains(., 'allstar')]]/@title").extract()
            comment['time'] = sel.xpath(".//span[@class='comment-info']/span[@class[contains(., 'comment-time')]]/@title").extract()
            comment['film_name'] = [" ".join(filmName)]
            comment['source'] = ','.join(self.allowed_domains)
            yield comment
        nextPage = response.xpath("//div[@id='paginator']/a[@class='next']/@href").extract_first()
        if(nextPage):
            nextUrl = response.request.url.split('?')[0] + ''.join(nextPage)
            self.logger.info("Next search page url is {}".format(nextUrl))
            yield Request(url=nextUrl, 
                    cookies = self.COOKIES,
                    callback=self.parse)
