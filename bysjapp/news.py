import requests,json
from lxml import etree
from lxml import html
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
                textsrc=textsrc.replace('https://petssky.com/news/world-','')

                item = {}

                item['imgsrc']=imgsrc
                item['title']=title
                item['textsrc']=int(textsrc)
                print(item)
                self.info_list.append(item)
class news:
    def __init__(self,url):
        self.url = "https://petssky.com/news/world-"+url
        self.info = ''
        self.title=''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.parse()
        # 请求url，获取页面内容，返回一个element对象

    def get_xpath(self, url):
        response = requests.get(url, self.headers)
        return etree.HTML(response.text)

    def get_text(self, text):
        if text:
            return text[0]
        return ''

    def parse(self):
        # https://www.qiushibaike.com/hot/page/2/

        html0 = self.get_xpath(self.url)
        main= html0.xpath('//*[@id="main"]/article')
        self.title=self.get_text(main[0].xpath('.//header/h1/text()'))
        plist= html0.xpath('/html/body/div[2]/div[2]/div[1]/main/article/div/div[2]/p')
        item={}
        body=[]
        for p in plist:
            a=self.get_text(p.xpath('text()'))
            b=self.get_text(p.xpath('.//text()'))
            img=self.get_text(p.xpath('.//img/@src'))
            if a==b:
                c=a
            else:
                c=b+a
            item.update(p=c,img=img)
            body.append(item)
            item={}
        print(body)
        self.info=body


