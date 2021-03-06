#! --coding:utf-8-- !# 
import hashlib
import random

f_length = 2 # bytes
g_length = 3#注意两个函数迭代的长度是不一样的
fg_blocksz = 16
f_initial = 'lo'
g_initial = 'lol'
#这个在single 的基础上就是多加了一个函数，原来的一个c变成了c_f,c_g
def C_f(m, H):
    r = hashlib.md5(H + m).digest()[:f_length]
    return r

def C_g(m, H):
    # just truncated md5
    r = hashlib.md5(H + m).digest()[:g_length]
    return r

def pad(m):#这个函数就是把m分成块
    for i in range(0, len(m), fg_blocksz):
        yield m[i:i+fg_blocksz]
    yield 'length:%d' % (len(m))

def generic_h(m, initial, C): #这个是返回对每个块迭代的结果，c是算法，代表c_f,或者c_g
    H = initial

    for block in pad(m):
        H = C(block, H)
    return H

def f(m):
    return generic_h(m, f_initial, C_f)
def g(m):
    return generic_h(m, g_initial, C_g)
def h(m):
    return f(m) + g(m)

def random_block(): #生成随机值
    return ''.join(chr(random.getrandbits(8)) for i in range(fg_blocksz))

def internal_collide(H, C): #得到碰撞，跟single中基本一样
    x = random_block()

    xH = C(x, H)
    while True:
        y = random_block()
        yH = C(y, H)
        if xH == yH and x != y:
            return x, y, xH, yH

def crosscheck(found, H):
    # 跟single中差不多的横向检查
    left = ''.join(x[0] for x in found)
    right = ''.join(x[1] for x in found)
    assert H(left) == H(right)

def generate_messages(found):
    if len(found) == 0:
        yield ''
    else:
        x, y = found[0]
        for suffixes in generate_messages(found[1:]):
            yield x + suffixes
            yield y + suffixes

def find_dual_collision(): #找到碰撞并且保存
    H_f = f_initial
    found = []
    for i in range(g_length * 8):
        # 生成一个大的碰撞区域
        x, y, xh, yh = internal_collide(H_f, C_f)
        found.append((x, y))
        H_f = xh

    crosscheck(found, f)

    #如果找到碰撞就提示
    check = {}
    for msg in generate_messages(found):
        gh = g(msg)

        collision = check.setdefault(gh, msg)
        if collision != msg: #这里会提示是否找到碰撞
            assert h(collision) == h(msg)
            print 'found collision after', len(check), 'g tests'
            break
    
if __name__ == '__main__':
    find_dual_collision()