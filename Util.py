import time
import hashlib
'''
工具类
'''

# 计算一个字符串的hash
def algo_sha256(str):
    sha256 = hashlib.sha256()
    sha256.update(str.encode('utf-8'))
    hash = sha256.hexdigest()
    return hash

#  获得一个对应格式时间的时间戳
def algo_getTimestamp(str_time):
    timestamp = time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
    return timestamp
# 获得当前时间的时间戳
def getNowTimestamp():
    now = time.mktime(time.localtime(time.time()))
    return now





