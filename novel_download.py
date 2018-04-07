# -*- coding: utf-8 -*-

from lxml import etree
import requests
import os

# 传入解析完的小说详情页面，返回小说基本信息
def getNovelInfo(page):
    novel_name_xpath = '//*[@id="info"]/h1/text()'
    novel_name = page.xpath(novel_name_xpath)[0]
    novel_author_xpath = '//*[@id="info"]/p[1]/text()'
    novel_author = page.xpath(novel_author_xpath)[0]
    novel_category = category
    update_time_xpath = '//*[@id="info"]/p[3]/text()'
    update_time = page.xpath(update_time_xpath)[0]
    latest_chapter_xpath = '//*[@id="info"]/p[4]/a/text()'
    latest_chapter = '最新章节：' + page.xpath(latest_chapter_xpath)[0]
    novel_intro_xpath = '//*[@id="intro"]/p/text()'
    novel_intro = page.xpath(novel_intro_xpath)[0]
    return novel_name + '\n' + novel_category + '\n' \
            + novel_author + '\n' + update_time + '\n' \
            + latest_chapter + '\n' + novel_intro + '\n'

# 传入小说详情页面，返回小说目录的链接列表
def getNovelChapter(page):
    chaper_link = []
    chaper_title = []
    chaper_count = 1
    link = 'init'
    title = ''
    while link != '':
        link_xpath = '//*[@id="list"]/dl/dd[{}]/a/@href'.format(str(chaper_count))
        title_xpath = '//*[@id="list"]/dl/dd[{}]/a/text()'.format(str(chaper_count))
        try:
            link = page.xpath(link_xpath)[0]
            title = page.xpath(title_xpath)[0]
            chaper_link.append(link)
            chaper_title.append(title)
        except IndexError:
            print('章节读取完毕')
            break
        finally:
            chaper_count = chaper_count+1
    return chaper_link, chaper_title

# 获取小说内容并写入文件
def getChapter(novel_page, novel_file):
    links, titles = getNovelChapter(novel_page)
    for link,title in zip(links, titles):
        url = root_url + link
        html = requests.get(url)
        html.encoding = 'utf-8'
        page = etree.HTML(html.content)
        content_xpath = '//*[@id="content"]/text()'
        content = page.xpath(content_xpath)
        con = ''
        for para in content:
            if para != '\r\n':
                con = con + para
        print(con)
        with open(novel_file, 'a', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write(con)



if __name__ == '__main__':

    main_url = 'http://www.biquge.com.tw/paihangbang/allvote.html'
    root_url = 'http://www.biquge.com.tw'

    # html = requests.get(main_url).text.encode('iso-8859-1').decode('gbk')
    # 排行榜页面
    html = requests.get(main_url)
    html.encoding = 'utf-8'
    page = etree.HTML(html.content)

    novel_html = ''
    novel_page = ''

    for i in range(2, 4):
        root_xpath = '//*[@id="main"]/div[{}]'.format(str(i))
        category_xpath = root_xpath + '/h3/text()'
        category = page.xpath(category_xpath)[0]
        print(category + '...')
        dir_path = category
        if os.path.exists(dir_path) == False:
            os.mkdir(dir_path)
        for j in range(1, 3):
            novel_xpath = root_xpath + '/ul/li[{}]/a'.format(str(j))
            novel_title = novel_xpath + '/text()'
            novel_link = novel_xpath + '/@href'
            print(novel_title)
            # 小说详情页面
            novel_url = page.xpath(novel_link)[0]
            novel_title = page.xpath(novel_title)[0]
            novel_html = requests.get(novel_url)
            novel_html.encoding = 'utf-8'
            novel_page = etree.HTML(novel_html.content)
            # 获取小数详情（简介、作者、最新章节等信息）
            novel_info = getNovelInfo(novel_page)
            # 创建存放小说的文本文件
            novel_file = dir_path + '/' + novel_title + '.txt'
            # 写入小说小说基本信息
            with open(novel_file, 'w', encoding='utf-8') as nov:
                nov.write(novel_info)
            # 读取小说内容
            getChapter(novel_page, novel_file)
