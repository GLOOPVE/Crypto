# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
import random

#aes cbc类
class aescbc:
    def __init__(self):
        self.iv=random._urandom(16)
        self.key=random._urandom(16)

    #设置iv
    def setiv(self,iv):
        self.iv=iv

    #获取iv
    def getiv(self):
        return self.iv

    #异或
    def xor(a,b):
        if len(a)!=len(b):
            return ""

        temp=""
        for i in range(len(a)):
            temp+=chr(ord(a[i])^ord(b[i]))
        return temp

    #给明文加padding
    def add_pad(self,a):
        padlength=16-(len(a)%16)
        temp=a+chr(padlength)*padlength
        return temp

    #单block aes加密器
    def aes(self,iv,plaintext):
        cipher=AES.new(self.key,AES.MODE_ECB,self.iv)
        ct=cipher.encrypt(plaintext)
        return ct.encode("hex")

    #cbc mac计算
    def cbc_mac(self,plaintext):
        if len(plaintext)%16!=0:
            return str(len(plaintext))
        cipher=AES.new(self.key,AES.MODE_ECB,self.iv)
        ct=cipher.encrypt(plaintext[0:16])
        for i in range(16,len(plaintext),16):
            cipher=AES.new(self.key,AES.MODE_ECB,ct)
            ct=cipher.encrypt(plaintext[i:i+16])
        return ct.encode("hex")

if __name__ == "__main__":
    a=aescbc()
    message="from=10&to=20&amount=100000000"
    #原文
    message=a.add_pad(message)
    print "Origin message:"+message
    print "Origin mac:"+a.cbc_mac(message)
    #计算原文的mac

    forgemessage="from=10&to=21&amount=100000000"
    forgemessage=a.add_pad(forgemessage)
    iv=a.getiv()
    forgeiv=iv[:12]+chr(ord(iv[12])^ord('1')^ord(message[12]))+iv[13:]
    #修改iv
    a.setiv(forgeiv)

    print "Forge message:"+forgemessage
    print "Forge mac:"+a.cbc_mac(forgemessage)
    #修改iv后对原文的mac

    message="from=10&tx_list=11:100;12:200"
    message=a.add_pad(message)
    mac=a.cbc_mac(message)
    #原文的mac
    print "Origin message:"+message
    print "Origin mac:"+mac

    pad="21:100000000"
    forgemac=a.aes(mac[-16:],a.add_pad(pad))
    #取上一段密文为iv，进行单次aes加密
    print "pad:"+pad
    print "Forge mac:"+forgemac

    print "Dodgey message:"+message+a.add_pad(pad)
    print "Dodgey mac:"+a.cbc_mac(message+a.add_pad(pad))
    #原文加上padding的mac值
    

    
    
        
