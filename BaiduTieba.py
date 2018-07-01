# -*- coding:utf-8 -*-
import requests,os,json
import sys
from lxml import etree
from User_agent import User_Agt
from time import time
from threading import Thread

class BaiduTieba_spider(object):
    ''''百度贴吧'''
    def __init__(self,name,start_page,end_page):
        self.url = 'https://tieba.baidu.com/f?'
        self.headers =User_Agt()
        self.name = name
        self.start_page = start_page
        self.end_page = end_page
        # self.name = input('请输入贴吧名：')
        # self.start_page = int(input('请输入开始页：'))
        # self.end_page = int(input('请输入结束页：'))
        self.num = 0
        self.page_file = ''


    def _get_page(self):
        '''获取页码'''
        # 遍历起始页
        # for pn in range(self.start_page,self.end_page+1):
        #     page = (pn-1) * 50

        # 获取页码列表
        page = [(pn-1)*50 for pn in range(self.start_page,self.end_page+1)]
        print(page)
        return page

    def _get_req_data(self):
        '''获取请求参数'''

        print('get_req_data')
        parmans = {
            'kw':self.name,
            'pn':self.start_page,
            'ie':'utf-8'
        }
        # 贴吧请求，
        resp = requests.get(self.url,params=parmans,headers =self.headers)
        with open('123.html','wb') as f:
            f.write(resp.content)
        resp = resp.text
        html = etree.HTML(resp)
        # 获取当前页中的所有帖子
        image_url = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
        # print(image_url)
        # print(len(image_url))
        # 遍历取出列表的每一个帖子，单独访问
        if not image_url:
            print('无数据')
            return

        for url in image_url:
            img_url = 'https://tieba.baidu.com'+ url

            self.get_image_data(img_url)


    def get_image_data(self,img_url):
        '''获取每个帖子的图片url'''

        try:
            image_html = requests.get(img_url,headers =self.headers)
            image_html = image_html.text
        except Exception as e:
            print(e)
            return

        image_url = etree.HTML(image_html)
        image_list = image_url.xpath('//img[@class="BDE_Image"]/@src')
        # 获取到的每个帖子的所有图片
        for image in image_list:

            self.save_iamge(image)

    def save_iamge(self,image):
        '''保存每张图片到本地'''
        data = requests.get(image,headers=self.headers) # 请求图片
        image_name = image.split('/')[-1] # 获取图片名


        file_path = os.path.join(self.name,self.page_file,image_name) #拼接存储路径
        with open(file_path,'wb') as f:
            f.write(data.content)
        # 保存数据

        self.num +=1
        print('第{}张'.format(self.num))

    def run(self):
        '''逻辑处理'''
        strat_time = time()
        if not self.name in os.listdir('./'):
            os.mkdir(self.name)
        # 获取总页码
        pages = self._get_page()
        # 1.获取参数
        thd_list =[]
        for page in pages:
            print(page)
            self.page_file = str(pages.index(page))

            if not self.page_file in os.listdir('./{}'.format(self.name)):
                os.mkdir('./{}/{}'.format(self.name,self.page_file))

            self.start_page = page

            # self._get_req_data()
            # 多线程爬去
            thd = Thread(target=self._get_req_data)
            thd.start()
            thd_list.append(thd)

        for thd in thd_list:
            print(123)
            thd.join()
        end_time = time()
        print('{}'.format(strat_time - end_time))
        print('----爬取完毕----共计{}'.format(self.num))



if __name__ == '__main__':
    name = sys.argv[1]
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])

    tb = BaiduTieba_spider(name,start_page,end_page)
    tb.run()





