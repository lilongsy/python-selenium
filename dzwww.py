# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys


# 采集列表页
def collect_list(bs):
    lists = []
    url_list = []
    # 分页
    i = 1
    while i <= 1:
        list = bs.find_elements_by_css_selector(".tuwen .style")
        for l in list:
            try:
                url = l.find_element_by_tag_name("a").get_attribute("href")
                #print url
                url_list.append(url)
            except Exception, e:
                #print e
                continue
        bs.find_element_by_link_text(u"下一页").click()
        time.sleep(2)
        i += 1
    return url_list

    
# 采集内容页
def collect_content(bs, url_list):
    i = 1
    content_list = []
    for u in url_list:
        print u
        bs.get(u)
        time.sleep(2)
        try:
            content = bs.find_element_by_css_selector(".TRS_Editor").get_attribute("innerHTML")
            title = bs.find_element_by_css_selector("h2").text
            publishTime = bs.find_element_by_xpath("//meta[@name='publishdate']").get_attribute("content")
            content_list.append({"url":u, "content":content, "title":title, "publishTime":publishTime})
        except Exception, e:
            print e
            continue
        finally:
            # 限制运行次数,方便测试
            if i >= 2:
                break
            i += 1
    return content_list
   
   
def save_content(content_list):
    for content in content_list:
        print ""
        print content['url']
        print content['title']


# 主函数
def main():
    bs = webdriver.Firefox()
    bs.maximize_window()
    bs.get("http://sd.dzwww.com/sdnews/")
    time.sleep(2)
    url_list = collect_list(bs)
    content_list = collect_content(bs, url_list)
    save_content(content_list)
    bs.quit()
    
    
main()
