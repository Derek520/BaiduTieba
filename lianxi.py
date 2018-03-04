# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# 创建 Beautiful Soup 对象
soup = BeautifulSoup(html)

# 打印出title标签
print(soup.title)

# 打印出第一个p标签
print(soup.p)

# 打印出第一个a标签
print(soup.a)

# 打印head标签的内容
print(soup.head)

# 打印出来的结果是整个boby里面的所有标签
print(soup.body)

# <class 'bs4.element.Tag'> 是这个类型，tag有两个属性 一个name,一个attrs
print(type(soup.p))

print("*" * 30)

# 这个输出的是[document]
print(soup.name)

# 输出标签名字title
print(soup.title.name)
# 输出标签head名字
print(soup.head.name)

# 输入一个空字典，是因为title没写属性
print(soup.title.attrs)

# 是把标签里的所有属性打印出来，会得到一个字典型数据
print(soup.p.attrs)

# 获取标签属性值,以下三种方法获取的结果一样
print(soup.p.attrs['class'])
print(soup.p['class'])
print(soup.p.get('class'))

# 修改属性值
soup.p['class']='hei'
print(soup.p)  # 查看修改后的结果

# 删除属性值
del soup.p['class']
print(soup.p)  # 查看删除后的属性值

# 获取标签的内容  .string
print(soup.title.string)
# 获取p标签的内容
print(soup.p.string)
# 获取a标签的内容
print(soup.a.string)

# 直接子节点 ：.contents .children 属性
# contents是获取该标签下所有子标签,返回的结果是一个列表
print(soup.head.contents)
# 取出boby标签的儿子标签
print(soup.body.contents)

' .children 看一下，可以发现它是一个 list 生成器对象' \
'它返回的不是一个 list，不过我们可以通过遍历获取所有子节点'

# .children 返回的是一个生成器
print(soup.head.children)

# .children结果是一个生成器，可以遍历取出每个元素结果
for child in soup.body.children:
    print(child)

print('-' * 30)
# 所有子孙节点: .descendants 属性
print(soup.descendants)

for descdan  in soup.descendants:
    print(descdan)

"""
find_all(name, attrs, recursive, text, **kwargs)
括号里面的参数：name是指标签名，查找所有的该标签，字符串会被自动忽略
"""
# 查找文档中所有b标签，返回结果是一个列表
print(soup.find_all('b'))

# 查找文档中所有a标签,返回结果是一个列表
print(soup.find_all('a'))

# 传入正则表达试，查找包含以b开头的标签
for tag in soup.find_all(re.compile('b')):
    # 输出标签名字
    print(tag.name)

# 如果传入列表,满足列表中任意一个的标签
for tag in soup.find_all(['a','b']):
    print(tag.name)

# 如果keyword 参数，是查找属性class等于sister的标签
print(soup.find_all(class_='sister'))

print(soup.find_all(id='link1'))

# 搜索文档中的字符串内容
print(soup.find_all(text=["Tillie", "Elsie", "Lacie"]))

# 搜索文本中包含Dormouse的字符串
print(soup.find_all(text=re.compile("Dormouse")))

# css选择器
'用到的方法是 soup.select()，返回类型是 list'

print(soup.select('.sister'))
print(soup.select('p'))
print(soup.select('#link1'))
# 组合查找 意思查找p标签中id属性等于link2的标签
print(soup.select('p #link2'))
# 直接子标签查找，则使用 > 分隔
print(soup.select('head > title'))

# 属性查找 标签必须和属性在同一个节点，不能用空格
print(soup.select('a[class="sister"]'))

print(soup.select('p a[href="http://example.com/elsie"]'))

# 在使用select情况下,使用get_text()获取内容
soup = BeautifulSoup(html,'lxml')

print(soup.select('title')[0].get_text())

for tag in soup.select('a'):
    print(tag.get_text())
