# -*- coding:utf-8 -*-

import zlib
import salsa20
import random

#获取request，压缩与加密
#加密使用salsa20，请先pip install salsa20
def getrequest(param):
    request="POST / HTTP/1.1\nHost: hapless.com\nCookie: sessionid=TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE=\nContent-Length:"+str(len(param))+"\n"+param
    compress=zlib.compress(request,9)
    #最高级别压缩
    encrypt=salsa20.Salsa20_xor(compress,random._urandom(8),random._urandom(32))
    return encrypt

#sessionkey大小
size=44

#所有可能的值
possc=()
for i in range(26):
    possc=possc+(chr(ord('a')+i),)
    possc=possc+(chr(ord('A')+i),)
for i in range(10):
    possc=possc+(str(i),)
possc=possc+('=',)
print possc

#破解得到的字符串
brokenstring="sessionid="

#遍历size次
for i in range(size):
    #标志，| 符号不属于可能的值
    winningchar='|'
    temp=brokenstring+winningchar
    temp=getrequest(temp)
    #设定最大的size
    winningsize=len(temp)
    #对于所有可能的值进行尝试
    for each in possc:
        test=brokenstring+each
        result=getrequest(test)
        #得到size最小的字符
        if len(result)<winningsize:
            winningsize=len(result)
            winningchar=each
    #如果没有最小的字符
    if winningchar=='|':
        #随机加入一段垃圾
        temp="qwertyqwerty"+brokenstring+winningchar
        temp=getrequest(temp)
        #加入垃圾后的size
        winningsize=len(temp)
        for each in possc:
            test="qwertyqwerty"+brokenstring+each
            result=getrequest(test)
            #得到size最小的值
            if len(result)<winningsize:
                winningsize=len(result)
                winningchar=each
    #还是拿不到最小的size
    if winningchar=='|':
        print "wtf"
        exit(0)
    brokenstring+=winningchar
print brokenstring
    
