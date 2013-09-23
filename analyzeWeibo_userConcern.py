#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'
__author__ = 'Zhang Xigang(xigangzhang@gmail.com)'

'''
 analyze user issues ,find his top N keywords ,you need provide uid what you want to analyze,need provide sina app key for use weibo api.
'''

import urllib2
import re
import sys,string
sys.path.append("../")


import jieba
import jieba.posseg as pseg
jieba.initialize()



__appKey__ = xxxxxxx # sina appkey

__keyWordNum__ = 40

__meaninglessKeywordsDictFileName__ = "meaninglessKeywordDict.txt"
   
# This function is to get the data of the given user in weibo     
# notice: the system only provide the lateset 200 weibo of one user    
def getUserData(user_id):     
  # the url to get the data     
  url = "http://api.t.sina.com.cn/statuses/user_timeline.xml?source=%d&user_id=%d&count=200"%(__appKey__, user_id)   

  # print url    
  strWeibo = urllib2.urlopen(url)   
  return strWeibo.read()

# seg the str and get top N keywords,
# strWeibo : weibo text
# mlkwStr : some word to discard
def getKeyWords(strWeibo,mlkwStr):
  words = pseg.cut(strWeibo)  
  keywordDict = {}   
  for w in words:      
      if len(w.word) > 1 and w.flag.startswith("n") : # other condisions : or w.flag.startswith("v") or w.flag.startswith("a")
          #print  w.word,"/",w.flag
          if(keywordDict.has_key(w.word)):
              keywordDict[w.word] += 1        
          else:
              keywordDict[w.word] = 1

  #print("-----------------------end of---pseg.cut()----------------------------")            
  #printCollection(keywordDict)
  #print("--------------------------keywords()----------------------------")
  sortedItems=sortDictByValues(keywordDict)
  size=len(sortedItems)
  keywordsText=""
 
  if(size >0):
     countor =0
     while countor < __keyWordNum__ :
           if (size-1-countor) >= 0 :
             #print sortedItems[size-1-countor],countor
             if  mlkwStr.find(sortedItems[size-1-countor]) == -1 :
               keywordsText = keywordsText +" "+ sortedItems[size-1-countor]+ "-("+ str(keywordDict[sortedItems[size-1-countor]])+")"               
             countor += 1

  return keywordsText


#sort a dict by value,return a list of key after sorted
def sortDictByValues(adict):
    items = adict.items() 
    backitems = [[v[1],v[0]] for v in items] 
    backitems.sort()    
    return [ backitems[i][1] for i in range(0,len(backitems))]

# get content of each weibo
def getWeiboText(origStr):
    weiboText=""
    p = re.compile('<text>([^<>])*</text>')
    m = p.search(origStr)
    while m :
      #print m.group()
      weiboText = weiboText+m.group().replace("<text>","").replace("</text>","")+"\n"
      origStr = origStr.replace(m.group(),"")
      m = p.search(origStr)
    return weiboText

  
# readin to discard words
def getMeaninglessKeywordsDict():
  inputStr =  open(__meaninglessKeywordsDictFileName__,"rb").read()
  return inputStr.decode("utf-8")


def main():

    userArray= [1222430350,1197161814,1649005320,1182391231,1182389073,1189591617]
    resultTotal =""
    mlkwStr = getMeaninglessKeywordsDict()

    for uid in userArray:    
      origStr = getUserData(uid)
      #print '---------------------------------------original------------------------------------'
      #print origStr
      print  uid,'------------------his top', __keyWordNum__ ,' keywords of latest 200 weibos :'
      resultTotal += str(uid) + '------------------his top'+ str( __keyWordNum__) +' keywords of latest 200 weibos :\n'

      weiboText = getWeiboText(origStr)
      #print weiboText
      topKeyWords =getKeyWords(weiboText,mlkwStr)
      print topKeyWords
      
      resultTotal += topKeyWords.encode("utf-8")
      resultTotal += '-----------------------------------------end--------------------------------------\n'
      print '-----------------------------------------end--------------------------------------'

    # save the result        
    f = file('resultTotal.txt', 'w')
    f.write(resultTotal)
    f.close()


    


if __name__ == '__main__':
    main()
