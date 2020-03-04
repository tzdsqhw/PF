import requests,json
from lxml import etree

class chongwu:
    def __init__(self,url):
        self.url = url
        self.info_list = []
        self.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.parse()
    #请求url，获取页面内容，返回一个element对象
    def get_xpath(self,url):
        response = requests.get(url,self.headers)
        return etree.HTML(response.text)
    def get_text(self,text):
        if text:
            return text[0]
        return ''
    def parse(self):
        #https://www.qiushibaike.com/hot/page/2/

            html = self.get_xpath(self.url)
            div_list = html.xpath('//*[@id="main"]/article')
            for i in range(0,6):
                # 图片链接：
                imgsrc = self.get_text(div_list[i].xpath('.//figure/a/img/@src'))
                # print(content)
                # 题目
                title = self.get_text(div_list[i].xpath('.//header/h2/a/text()'))
                textsrc = self.get_text(div_list[i].xpath('.//header/h2/a/@href'))


                item = {}

                item['imgsrc']=imgsrc
                item['title']=title
                item['textsrc']=textsrc
                self.info_list.append(item)

