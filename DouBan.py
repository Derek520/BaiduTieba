# -*- coding:utf-8 -*-
import requests,json
from jsonpath import jsonpath
from User_agent import User_Agt
import pandas



class DouBan(object):
    '''豆瓣电视剧'''

    __list1 = []
    def __init__(self):
        self.url = 'https://movie.douban.com/j/search_subjects?'
        self.tags_url ='https://movie.douban.com/j/search_tags?type=tv&tag=%E7%BE%8E%E5%89%A7&source='
        self.tag = []
        self.page_start = 0
        self.headers = User_Agt()
        self.recommend = 'recommend'
        self.num = 1


    def _tags_url(self):
        '''tags'''
        resp = requests.get(self.tags_url,headers=self.headers)
        tags_str = resp.content.decode()
        tags_json = json.loads(tags_str)
        self.tag.append(jsonpath(tags_json,'$..tags'))

    def _parmans(self):
        '''请求参数'''
        params = {
            'tag': self.tag_name,
            'page_start':self.page_start,
            'sort':self.recommend
        }
        err = self.get_url(params)
        return err

    def get_url(self,params):
        '''请求相应'''
        try:
            resp = requests.get(self.url,params=params,headers =self.headers)
            str_data = resp.content.decode()
            json_data = json.loads(str_data)
            item ={}
            item['title'] = jsonpath(json_data,'$..title')
            item['rate'] = jsonpath(json_data,'$..rate')
            item['url'] = jsonpath(json_data,'$..url')
            # item['tag'] = jsonpath(json_data,'$..tag')

        except Exception as e:
            return 'err'
        # print(item)
        # DouBan.__list1.append(item)
        if len(item['title'])>0:
            self.__save_data(item)


    def __save_data(self,item):
        '''保存数据'''

        for i in range(len(item['title'])):
            dict = {}
            dict['tag'] = self.tag_name
            dict['title']=item['title'][i]
            dict['rate'] = item['rate'][i]
            dict['url'] = item['url'][i]
            print('--{}-----保存数据第{}条-----------'.format(self.tag_name,self.num))
            # print(dict)

            if dict in DouBan.__list1:
                continue
            DouBan.__list1.append(dict)
            self.num += 1
    def run(self):
        '''逻辑处理'''
        self._tags_url()

        # tag = self.tag[0][0][1]
        for tag in self.tag[0][0]:
            self.tag_name = tag
            page = 0
            while page<10:

            # for page in range(10):

                self.page_start =page
                print(self.page_start,self.tag_name)
                self.headers = User_Agt()
                data = self._parmans()
                if data=='err':
                    break
                page+=1
        data = pandas.DataFrame(DouBan.__list1)
        data.to_csv('豆瓣电视剧.csv',encoding='gb18030')
        print('----------<爬取完毕>-------')


if __name__ == '__main__':
    db = DouBan()
    db.run()