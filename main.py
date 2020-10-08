from BlockChain import *
from Miner import *
import threading
import copy
import time
# 矿工线程
class minerThread (threading.Thread):
    def __init__(self, miner, globalchain):
        threading.Thread.__init__(self)
        self.miner = miner
        self.globalchain = globalchain

    def run(self):
        self.miner.mine_block(self.globalchain)

# 记录线程
class logThread(threading.Thread):
    def __init__(self, globalchain,filePath):
        threading.Thread.__init__(self)
        self.globalchain = globalchain
        self.filePath = filePath

    def run(self):
        while True:
            time.sleep(1)
            f = open(self.filePath, mode='w', encoding='utf-8')
            self.globalchain.showInfo(f)
            f.close()




if __name__ == "__main__":
    globalChain = BlockChain(difficulty=1)  # difficulty 难度为POW部分，区块hash前面为0的个数
    # timedelta 参数调整矿工挖矿间隔时间，时间越长，矿工挖矿速度越慢。用来模拟现实中矿工因设备不同而造成的速度不同
    miner1 = Miner(minerID="1",localChain=copy.deepcopy(globalChain),timedelta=1)
    miner2 = Miner(minerID="2", localChain=copy.deepcopy(globalChain),timedelta=1)
    miner3 = Miner(minerID="3", localChain=copy.deepcopy(globalChain),timedelta=1)

    # 创建新线程
    thread1 = minerThread(miner1,globalChain)
    thread2 = minerThread(miner2,globalChain)
    thread3 = minerThread(miner3, globalChain)
    # threadlog 用来打印区块链的区块信息，每一秒更新一次，并且写入log.txt文件
    threadLog = logThread(globalChain,"log.txt")

    # 开启新线程
    thread1.start()
    thread2.start()
    thread3.start()
    threadLog.start()
    thread1.join()
    thread2.join()
    thread3.join()
    threadLog.join()


