
# 区块链交易类
class Transaction:
    def __init__(self, from_address="monk", to_address="DouShuai", amount=0,fee=0.005):
        '''
        初始化交易
        :param from_address: 交易发起方
        :param to_address: 交易接收方
        :param amount: 交易金额
        '''
        self.from_address = from_address
        self.to_address = to_address
        self.amount = min(amount,70)
        self.fee = fee
    # 序列化交易
    def serialize(self):
        return str(self.from_address)+str(self.to_address)+str(self.amount)+str(self.fee)

