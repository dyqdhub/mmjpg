#!/bin/python
# -*- coding:utf-8 -*-

import os
import urllib.request
from lxml import etree

from pyquery import PyQuery

url = "http://www.mmjpg.com/"

# 获取首页内容所有图片详情链接
response = urllib.request.urlopen(url, timeout=3)
html = response.read().decode('utf-8')
html_xml = etree.HTML(html)
imgurl_list = html_xml.xpath('//div[@class="pic"]/ul/li/a/@href')

#获取详情页图片
re = urllib.request.urlopen(url=imgurl_list[0])
img_html = re.read().decode('utf-8')

#获取详情页图片信息
img_html_xml = etree.HTML(img_html)
img_page = img_html_xml.xpath('//div[@id="content"]/a/@href')[0]
img_url = img_html_xml.xpath('//div[@id="content"]/a/img/@src')[0]
img_name = img_html_xml.xpath('//div[@id="content"]/a/img/@alt')[0]



def save_img(img_url):
    re_img = urllib.request.urlopen(img_url)
    re_img_by = re_img.read()
    file = open(img_url[-8:], 'wb')
    file.write(re_img_by)


