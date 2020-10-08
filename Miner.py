import time
import Util
from BlockChain import Block
import copy

'''
矿工类
'''
class Miner:
    def __init__(self,minerID,localChain,wallet=None,timedelta=1):
        '''

        :param minerID:  矿工ID
        :param localChain: 矿工本地存储的区块链信息（我们假定所有矿工类型均为全节点矿工）
        :param wallet:  TODO：钱包
        :param timedelta: 每次挖矿间隔时间，用来模拟挖矿速度
        '''
        self.minerID = minerID #
        self.localChain = localChain
        self.wallet = wallet
        self.randNum = 0    # 挖矿次数（我们认为计算一次hash为一次挖矿）
        self.timedelta = timedelta


    def mine_block(self,globalChain):
        '''
        挖矿函数
        :param globalChain: 全局区块
        :return:
        '''
        difficulty = self.localChain.difficulty

        while True:
            self.randNum += 1
            timestamp = Util.getNowTimestamp()
            # 构造区块
            block = Block(timestamp=timestamp,index=self.localChain.getChainLength()+1,previous_hash=self.localChain.getPreviousHash(),
                          nouce=self.randNum,minerID=self.minerID)
            # 如果满足挖矿难度要求，更新本地区块
            if block.hash[0: difficulty] == ''.join(['0'] * difficulty):
                self.localChain.chain.append(copy.deepcopy(block))
                print("bingo! miner" + str(self.minerID) +" 在第"+str(self.randNum) +"次尝试后成功挖到"+str(self.localChain.getChainLength())+"号区块")
            # 每一次挖矿后均查询全局区块并执行相应操作
            self.queryGlobalChain(globalChain)
            # 挖矿间隙，时间设置越短，越有可能出现两个区块同时挖出同一高度的情况
            time.sleep(self.timedelta)



    def queryGlobalChain(self,globalChain):
        '''
        查询全局区块链，并更新自己的本地区块链和全局区块链
        :param globalChain: 全局区块链
        :return:
        '''
        # 如果本地区块链高度小于全局区块链，那么证明本地区链块信息滞后，其他矿工已经挖出更高高度的区块链，所以更新本地区块链
        if self.localChain.getChainLength()<globalChain.getChainLength():
            self.localChain.updateChain(globalChain.chain)
        # 如果本地区块链高度大于全局区块链
        elif self.localChain.getChainLength()>globalChain.getChainLength():
            # 如果本地区块链高度恰好是全局区块链高度加1，且本地区块链是在全局区块链基础上进行挖矿，则更新全局区块
            if self.localChain.getChainLength()==globalChain.getChainLength()+1 and self.localChain.chain[-2].hash==globalChain.getPreviousHash():
                globalChain.updateChain(self.localChain.chain)
            else:
                self.localChain.updateChain(globalChain.chain)
        # 如果本地区块链高度等于全局区块链高度 【全网都没有挖出区块或者是两个miner同时挖到同一高度的区块，那么选择hash值小的】
        else:
            # 如果这个miner 挖出的区块hash小
            if self.localChain.getPreviousHash()<globalChain.getPreviousHash():

                globalChain.updateChain(self.localChain.chain)
                print("woo! miner" + str(self.minerID) + " 因为计算hash值小抢得了" + str(self.localChain.getChainLength()) + "号区块")

            # 全网都没有挖出区块
            elif self.localChain.getPreviousHash()==globalChain.getPreviousHash():
                pass
            # 如果这个miner 挖出的区块hash大
            else:
                self.localChain.updateChain(globalChain.chain)



    def checkBlock(self,block):
        '''
        验证区块信息
        :param block: 区块
        :return:
        '''
        raw_str = str(block.previous_hash) + str(block.timestamp) + str(block.transaction) + \
                  str(block.index) + str(block.nounce) + str(block.minerID)
        hash = Util.algo_sha256(raw_str)
        return hash==block.hash

    def checkBlockChain(self,blockChain):
        '''
        验证区块链信息
        :param blockChain: 区块链
        :return:
        '''
        chain = blockChain.chain
        if len(chain)==0 or not self.checkBlock(chain[0]): return False
        previous_hash = chain[0].hash
        for x in chain[1:]:
            if x.previous_hash!=previous_hash: return False
            elif not self.checkBlock(x): return False
            previous_hash = x.hash
        return True




