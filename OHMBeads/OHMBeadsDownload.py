#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-
#命令行在Terminal里执行，字符为乱码需先输入cpcy 65001,但是中文为第一个字符时，仍然为乱码,不懂为何
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import os
from os import path

SEARCH_LINK="http://www.ohmbeads.co.th/catalogsearch/result?order=sku&dir=asc&q=%s#page=%d"
INFO_FORMAT="%s\t%s\t%s\n"

downloadedBeads={};
IMAGES_FOLDER_PATH=''
INFOFILE_PATH=path.dirname(__file__)+'/BeadsInfo.txt'

def products_url(word,page):
    return SEARCH_LINK % (word,page)

def images_folder():
    global IMAGES_FOLDER_PATH
    if IMAGES_FOLDER_PATH != '':
        return IMAGES_FOLDER_PATH

    imageFolder=path.dirname(__file__)+'/beads_images'
    if not os.path.exists(imageFolder):
        os.mkdir(imageFolder)

    IMAGES_FOLDER_PATH = imageFolder+'/'
    return IMAGES_FOLDER_PATH

class bead:
    def __init__(self, name, link):
        self.__name = name
        self.__link = link
        self.__code = link[link.rfind('/', beg=0, end=len(link))+1:]

def do_request(word, page):
    global downloadedBeads
    source_code = urllib2.urlopen(products_url(word, page))
    # just get the code, no headers or anything
    plain_text = unicode(source_code.read(), 'utf-8')
    soup = BeautifulSoup(plain_text)
    processingBeads ={};
    for image in soup.findAll(attrs={'class': 'product_image'}):
        name = image.get('alt')
        if not downloadedBeads.has_key(name):
            processingBeads[name] = image.get('src') #name->jpg link

    if len(processingBeads) != 0:
        infofile = open(INFOFILE_PATH, 'a')
        for product in soup.findAll(attrs={'class': 'product-image'}):
            beadName = product.get('title')
            if processingBeads.has_key(beadName):
                beadLink = product.get('href')
                pos = beadLink.rfind('/', 0, len(beadLink))
                beadCode = beadLink[(pos+1):]
                imageFile = images_folder() + beadCode + '_' + beadName + '.jpg'
                urllib.urlretrieve(processingBeads[beadName], imageFile)
                infofile.write(INFO_FORMAT % (beadCode, beadName, beadLink))
        infofile.close()

do_request('aa',1);
do_request('aa',2);
