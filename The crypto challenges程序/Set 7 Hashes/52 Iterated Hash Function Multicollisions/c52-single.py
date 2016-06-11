#! --coding:utf-8-- !# 
import hashlib
import random

lolhash_length = 2 # bytes
lolhash_blocksz = 16
lolhash_initial = 'lo'

def C(m, H): #这个函数是把m和M一起求md5的前2位
    # just truncated md5
    r = hashlib.md5(H + m).digest()[:lolhash_length]
    return r

def pad(m): #把m分块16个字节为一块
    for i in range(0, len(m), lolhash_blocksz):
        yield m[i:i+lolhash_blocksz]
    yield 'length:%d' % (len(m))
 
def lolhash(m):  #把m每个块求md5值的前2位作为H，并返回最后的H
    H = lolhash_initial

    for block in pad(m):
        H = C(block, H)
    return H

def random_block(): #生成16个8位2进制数
    return ''.join(chr(random.getrandbits(8)) for i in range(lolhash_blocksz))

lolhash_collide_calls = 0

def lolhash_collide(H):  #这个函数是找出计算md5之后前两位相同的字符串x和y，作为碰撞区域
   
    x = random_block()

    xH = C(x, H)
    while True:
        y = random_block()
        yH = C(y, H)
        if xH == yH and x != y:
            return x, y, xH, yH

def crosscheck(found): #横向检查

    H_left = H_right = lolhash_initial

    for i in range(len(found)): #检查迭代到最后一轮循环之后H的值是不是相等的
        left, right = found[i]
        H_left = C(left, H_left)
        H_right = C(right, H_right)

    assert H_left == H_right

    left = ''.join(x[0] for x in found)
    right = ''.join(x[1] for x in found)
    assert lolhash(left) == lolhash(right) #作用和上面的for循环一样，只是另一种方式实现

def f(n):
    # start off
    x, y, xh, yh = lolhash_collide(lolhash_initial) #先找出一个碰撞

    found = [(x, y)] #然后通过第一个找出的xh带入迭代中，找出剩下n-1个碰撞
    for i in range(1,n):
        x, y, xh, yh = lolhash_collide(xh)
        found.append((x, y))
    print found
    crosscheck(found) #这个函数是检测找出来的x和y是不是对的
    #通过这n对碰撞区域，可以构造出2^n对碰撞了
    print '\n found', len(found), 'pairs of internal collisions and we get ', 2 ** len(found), 'colliding messages'
    
if __name__ == '__main__':
    f(32)