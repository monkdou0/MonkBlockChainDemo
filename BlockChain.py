import time
import Util
from Transaction import Transaction
import copy

'''
区块类
'''
class Block:
    def __init__(self,timestamp,index,previous_hash,nouce,minerID,transaction=None):
        '''

        :param timestamp: 时间戳
        :param index: 区块高度
        :param previous_hash: 上个区块hash·
        :param nouce: 本区块的随机值
        :param minerID: 本区块miner的ID
        :param transaction: 交易信息
        '''
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.index = index
        self.nounce = nouce
        self.minerID = minerID
        self.transaction = Transaction(amount=index)
        self.hash = self.calculate_hash()

    # sha256算法计算本区块hash
    def calculate_hash(self):
        raw_str = str(self.previous_hash) + str(self.timestamp)+ str(self.transaction) + \
                  str(self.index)+str(self.nounce)+ str(self.minerID)
        hash = Util.algo_sha256(raw_str)
        return hash

    # 返回此区块的信息
    def showInfo(self):
        return "index:"+str(self.index)+" minerID"+str(self.minerID)+\
              " previous_hash:"+str(self.previous_hash)+\
              " hash:"+str(self.hash)+\
              " timestamp:"+str(self.timestamp)


'''
区块链类
'''
class BlockChain:
    def __init__(self,difficulty=2,miner_reward=100):
        '''

        :param difficulty:  区块链挖矿难度，difficulty 代表的是区块hash前面0的个数
        :param miner_reward: 区块链挖矿奖励
        '''
        self.chain = []  # 区块链的区块list
        #self.account = [] # TODO: 区块链账户
        self.difficulty = difficulty
        self.miner_reward = miner_reward
        #self.txpool = []  #TODO： 交易池
        self.create_genesis_block()  # 构建创世纪区块

    # 构建创世纪区块
    def create_genesis_block(self):
        time_str = '2020-10-01 00:00:00'
        timestamp = Util.algo_getTimestamp(time_str)
        genis = Block(timestamp=timestamp,index=0,previous_hash="df5d917b54707a716d9bf3d64e3626d9e3e611527972d51907fdc49f05b4c17a",nouce="0",minerID="0")
        self.chain.append(genis)

    # 获得此区块链当前最高高度的hash值
    def getPreviousHash(self):
        return self.chain[-1].hash
    # 获得区块链高度
    def getChainLength(self):
        return self.chain[-1].index
    # 更新区块链区块信息 （这发生在当2个miner同时计算出一个区块高度的区块时，选择hash更小的区块作为共识）
    def updateChain(self,chain):
        self.chain = copy.deepcopy(chain)
   # 打印区块链信息
    def showInfo(self,file):
        for x in self.chain:
            print(x.showInfo(),file=file)




