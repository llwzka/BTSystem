import json 
import os
from enum import Enum, unique
#----------------------------------
#需要进行传递的参数结构
#用空类可定义结构体

#读取json文件
class JsonConf:
    def load(self,path): 
        #调用例子print(tJsonConf().load("/home/lolfish/Desktop/test/contract_info/contract_info.json"))
        if not os.path.exists(str(path)):
            with open(str(path), 'w') as json_file:
                pass       
        with open(str(path)) as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {}
            return data


#行情接口数据类型
class Ticker:
    def __init__(self,date = None,time = None,o = 0,h = 0,l = 0,c = 0,v = 0):
        self.date=date
        self.time=time
        self.open=o
        self.high=h
        self.low=l
        self.close=c
        self.vol=v


#回测参数
class TestInfo:
    def __init__(self,cn = '',ccu = '',cc = 0,bd = '',ed = ''):
        self.contract_name = cn
        self.contract_cycle_unit = ccu
        self.contract_cycle = cc
        self.begin_date = bd
        self.end_date = ed

    

#合约参数
class ContractInfo:
    def __init__(self,sn = '',mr = 0,m = 0,mu = 0,f = 0,s = 0):
        self.strategy_name = sn
        self.margin_ratio = mr
        self.multiplier = m
        self.minimal_unit = mu
        self.fees = f
        self.slippage = s



#头寸方向
@unique
class Direction(Enum):
    Empty = 0
    Long = 1
    Short = -1

#交易实时状态参数
class MarketInfo:
    def __init__(self):
        #持仓方向状态，0为多头,1为空头，2为空仓
        self.direction = Direction.Empty
        #记录开仓价格
        self.open_price = 0 
        #当前的持仓手数
        self.market_amount = int(0)
        #起始资本金
        self.initial_capital = 0
        #盘中最高权益
        self.highest_interest = 0
        #是否开仓
        self.if_open = False
        #开仓手数
        self.open_amount = int(0)
        #平仓数量统计
        self.if_close = False
        #平仓手数
        self.close_amount = int(0)
    

class DelvOrder:
    def __init__(self,d = None,t = None,bs = ' ',oc = ' ',a = 0,p = 0):
        self.date = d
        self.time = t
        self.buy_or_sell = bs
        self.open_or_close = oc
        self.amount = a
        self.price = p 

class DynamicEquity:
    def __init__(self,d = None,t = None,de = 0):
        self.date = d
        self.time = t
        self.dynamic_equity = de

class DynamicRisk:
    def __init__(self,d = None,t = None,dr = 0):
        self.date = d
        self.time = t
        self.dynamic_risk = dr   

class DynamicRetreat:
    def __init__(self,d = None,t = None,dr = 0):
        self.date = d
        self.time = t
        self.dynamic_retreat = dr            

class LostPercent:
    def __init__(self,d = None,t = None,lp = 0):
        self.date = d
        self.time = t
        self.lost_percent = lp    

class IfEntrance:
    def __init__(self,d = None,t = None,ie = False):
        self.date = d
        self.time = t
        self.if_entrance = ie
