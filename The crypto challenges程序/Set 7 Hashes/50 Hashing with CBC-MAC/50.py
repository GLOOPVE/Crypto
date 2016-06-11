#coding:utf-8
import aes  #需要对每个块进行填充，没有办法调库，18题源代码
import os
mac_key = 'YELLOW SUBMARINE'
def aes_cbcmac(key, msg):#有填充计算mac
    cipher = aes.encryptData(key, msg, iv = '\0' * 16)
    return cipher[-16:]
def aes_cbcmac_nopad(key, msg):#无填充计算mac
    cipher = aes.encryptData(key, msg, iv = '\0' * 16, pad = False)
    return cipher[-16:]
def aes_ecb_decrypt(key, block):#计算调整模块
    adjustment = aes.AES().decrypt(map(ord, block), map(ord, key), len(key))
    return ''.join(chr(x) for x in adjustment)
def xor_block(a, b):  #模块异或
    return ''.join(chr(ord(a[i]) ^ ord(b[i])) for i in range(len(a)))

UNACCEPTABLE = ''.join(chr(x) for x in range(9)) + '\n'
def roughly_printable(msg):
    for m in msg:
        if m in UNACCEPTABLE:
			print 'bad', repr(m)
			return False
    return True

if __name__ == '__main__':
    good_code = "alert('MZA who was that?');\n"
    target_mac = '296b8d7cb78a243dda4d0a61d33bbdd1'.decode('hex')
    #找到不含控制模块的填充
    bad_code_prefix = "alert('Ayo, the Wu is back!');//asd"
    counter_format = '%08x'
    counter_sz = 4
    bad_pad = '\t' * 9
    # 添加填充 填充是 D(target_mac) ^ bad_mac
    adjustment = aes_ecb_decrypt(mac_key, target_mac)
    counter = 0x20202020
    while True:
        counter += 1 #模块加一
        counter_block = counter_format % counter
        bad_code = bad_code_prefix + counter_block.decode('hex')#调整后的输出js代码
        bad_mac = aes_cbcmac(mac_key, bad_code)
        # 添加填充模块给bad-code
        attack = bad_code + bad_pad + xor_block(bad_mac, adjustment)
        assert target_mac == aes_cbcmac_nopad(mac_key, attack)
        if roughly_printable(attack):#写html
            f = open('chengshabi.html', 'w')
            print >>f, '<html><body><script>'
            print >>f, attack
            print >>f, '</script></body></html>'
            f.close()
            print attack.encode('hex')
            break