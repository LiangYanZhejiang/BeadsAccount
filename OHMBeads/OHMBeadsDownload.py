#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-
#命令行在Terminal里执行，字符为乱码需先输入cpcy 65001,但是中文为第一个字符时，仍然为乱码,不懂为何
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import os
from os import path

#BeadsLink
#SEARCH_LINK="http://www.ohmbeads.co.th/catalogsearch/result?order=sku&dir=asc&q=%s&#page=%d"
SEARCH_LINK="http://www.ohmbeads.co.th/catalogsearch/result/index?dir=asc&order=sku&p=%d&q=%s"
LETTERS='abcdefghijklmnopqrstuvwxyz'

#Beads that already downloaded{name->1}
downloadedBeads={}
URLsMap={}

#Beads Downloaded info
INFOFILE_PATH=path.dirname(__file__)+'/BeadsInfo.txt'
URLs_File=path.dirname(__file__)+'/Beads_URLs.txt'
#beads infomation in file BeadsInfo.txt
#productCode    name    link
INFO_FORMAT="%s\t%s\t%s\n"

def products_url(word,page):
    print SEARCH_LINK % (page, word)
    return SEARCH_LINK % (page, word)

#Beads images folder
IMAGES_FOLDER_PATH=''
def images_folder():
    global IMAGES_FOLDER_PATH
    if IMAGES_FOLDER_PATH != '':
        return IMAGES_FOLDER_PATH

    imageFolder=path.dirname(__file__)+'/beads_images'
    if not os.path.exists(imageFolder):
        os.mkdir(imageFolder)

    IMAGES_FOLDER_PATH = imageFolder+'/'
    return IMAGES_FOLDER_PATH

#return = True: can get beads info from url, shoould try next page
def do_request(word, page):
    global downloadedBeads
    url = products_url(word, page)
    if URLsMap.has_key(url):
        return True;
    source_code = urllib2.urlopen(url)
    # just get the code, no headers or anything
    plain_text = unicode(source_code.read(), 'utf-8')
    soup = BeautifulSoup(plain_text)
    processingBeads ={};
    result = False
    for image in soup.findAll(attrs={'class': 'product_image'}):
        result = True
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
                imageFile = images_folder() + beadCode + '.jpg'
                urllib.urlretrieve(processingBeads[beadName], imageFile)
                infofile.write(INFO_FORMAT % (beadCode, beadName, beadLink))
                downloadedBeads[beadName]=1
        infofile.close()
        #Add url to URLs file
        urlsfile = open(URLs_File, 'a')
        urlsfile.write(products_url(word, page) + '\n')
        urlsfile.close()

    return result


def getDownloadedBeads():
    global downloadedBeads
    if os.path.exists(INFOFILE_PATH):
        infofile = open(INFOFILE_PATH, 'r')
        while 1:
            line = infofile.readline()
            if not line:
                break
            pos = line.find('\t',0, len(line))
            if pos > 0 :
                pos1 = line.find('\t', pos+1, len(line))
                downloadedBeads[line[pos+1:pos1]]=1
        infofile.close()

def getDownloadedURLs():
    global URLsMap
    if os.path.exists(URLs_File):
        urlsfile = open(URLs_File, 'r')

        while 1:
            line = urlsfile.readline()
            if not line:
                break
            if line != '':
                URLsMap[line]=1

        urlsfile.close()

getDownloadedBeads()
getDownloadedURLs()
print len(downloadedBeads)
print len(URLsMap)
for alp1 in LETTERS:
    for alp2 in LETTERS:
        page = 1
        while do_request(alp1+alp2,page):
            page +=1