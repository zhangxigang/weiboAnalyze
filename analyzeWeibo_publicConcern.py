#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'
__author__ = 'Zhang Xigang(xigangzhang@gmail.com)'

'''
 analyze public issues ,find top N keywords ,you need provide sina app key for use weibo api.
'''

import urllib2
import re
import sys,string
import types  
sys.path.append("../")


import jieba
jieba.initialize()

try:
    import json
except ImportError:
    import simplejson as json

__appKey__ = xxxxxxx # sina appkey

__keyWordNum__ = 40

__meaninglessKeywordsDictFileName__ = "meaninglessKeywordDict.txt"
   
# This function is to get the data of the given user in weibo     
# notice: the system only provide the lateset 200 weibo of one user    
def getWeiboData(count):     
  # the url to get the data     
  url = "https://api.weibo.com/2/statuses/public_timeline.json?source=%d&count=%d"%(__appKey__, count)     

  # print url    
  strWeibo = urllib2.urlopen(url)   
  return strWeibo.read()

def _parse_json(s):
    ' parse str into JsonDict '

    def _obj_hook(pairs):
        ' convert json object to python object '
        o = JsonDict()
        for k, v in pairs.iteritems():
            o[str(k)] = v
        return o
    return json.loads(s, object_hook=_obj_hook)

  
class JsonDict(dict):
    ' general json object that allows attributes to be bound to and also behaves like a dict '

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value
  

# seg the str and get top N keywords,
# strWeibo : weibo text
# mlkwStr : some word to discard
def getKeyWords(strWeibo,mlkwStr):
  words = ",".join(jieba.cut_for_search(strWeibo))
  print words 
  words = words.split(",")
  keywordDict= {}
  for w in words:
      print w,re.match("^[0-9]*$",w)
      
      if len(w) > 1 and (not re.match("^[0-9]*$",w)) : 
          if(keywordDict.has_key(w)):
              keywordDict[w] += 1        
          else:
              keywordDict[w] = 1

  #print("-----------------------end of---pseg.cut()----------------------------")            
  #printCollection(keywordDict)
  #print("--------------------------keywords()----------------------------")
  sortedItems=sortDictByValues(keywordDict)
  size=len(sortedItems)
  keywordsText=""

  end = __keyWordNum__

  if(size < end):
     end = size
 
  if(size >0):
     countor =0
     while countor < end :
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
def getWeiboText(weiboDict):
    weiboText=""
    for i in range(0,len(weiboDict.__getattr__("statuses"))-1):
      wb = weiboDict.__getattr__("statuses")[i]
      #print wb.__getattr__("text")
      weiboText += wb.__getattr__("text")+"\n"
    return weiboText

  
# readin to discard words
def getMeaninglessKeywordsDict():
  inputStr =  open(__meaninglessKeywordsDictFileName__,"rb").read()
  return inputStr.decode("utf-8")


def main():

    resultTotal =""
    mlkwStr = getMeaninglessKeywordsDict()

  
    origStr = getWeiboData(10)
    print '---------------------------------------original------------------------------------'
    #print origStr

    weiboDict = _parse_json(origStr)
    #print '--------------------------------------------------------------------------------'
    #print( weiboDict)
    #print '--------------------------------------------------------------------------------'
 
    #print '-----------------------------------------end--------------------------------------'
    weiboText = getWeiboText(weiboDict)
    print weiboText
    webKeyWords = getKeyWords(weiboText,mlkwStr)
    print '---------------------------------------------------------------------------------'
    print webKeyWords
    # save the result        
    f = file('webKeyWords.txt', 'w')
    f.write(webKeyWords.encode("utf-8"))
    f.close()

if __name__ == '__main__':
    main()
