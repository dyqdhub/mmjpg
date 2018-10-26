#!/bin/python
# -*- coding:utf-8 -*-

import os
import requests
from lxml import etree
from pyquery import PyQuery


url = "http://www.mmjpg.com/"


#下载图片并保存
def download_save(img_page_url,img_url,name):
    header = {
        'Referer': img_page_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    }
    file_name = img_url[-8:]
    img_rs = requests.get(img_url, headers=header)
    # print(img_rs.status_code)
    img_by = img_rs.content
    file = open('{}\{}'.format(name,file_name), 'wb')
    file.write(img_by)


#爬取首页所有图片的地址
def get_index_url(page):
    index_url_list = []
    for num in range(1, page+1):
        print("正在爬取第%s页" % str(num))
        if num == 1:
            index_page = url
        else:
            index_page = url + 'home/%s' % num
        re_index_html = requests.get(index_page)
        re_index_html.encoding="utf-8"
        index_html = re_index_html.text
        index_html_xml = etree.HTML(index_html)
        index_img_url_list = index_html_xml.xpath('//div[@class="pic"]/ul/li/a/@href')
        for l in index_img_url_list:
            index_url_list.append(l)
    return index_url_list

#获取图集页面的图片地址
def get_img_url(url_list):
    for url in url_list:
        re_img_html = requests.get(url)
        re_img_html.encoding="utf-8"
        img_html = re_img_html.text
        img_html_xml = etree.HTML(img_html)
        #获取图集的名称和页数，并循环页数
        img_html_name = img_html_xml.xpath('//div[@class="article"]/h2/text()')[0]
        print("正在爬取：%s" % img_html_name)
        os.mkdir(img_html_name)
        page_nu = img_html_xml.xpath('//div[@class="page"]/a[last()-1]/text()')[0]
        for nu in range(1, int(page_nu)+1):
            #拼接获得每页图片的URL
            img_page_url = url + '/' + str(nu)
            r_i_h = requests.get(img_page_url)
            r_i_h.encoding="utf-8"
            i_h = r_i_h.text
            i_h_x = etree.HTML(i_h)
            img_url = i_h_x.xpath('//div[@id="content"]/a/img/@src')[0]
            download_save(img_page_url,img_url,img_html_name)


if __name__ == '__main__':
    url_list = get_index_url(1)
    get_img_url(url_list)
