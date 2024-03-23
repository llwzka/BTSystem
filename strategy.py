import pandas as pd
import time
import numpy as np
import talib
import datetime
import strategy_original
import trader
import indicator
import datastruct


class Strategy(strategy_original.Strategy_original): 
    
    def __init__(self):
        #设置 
        self.initial_day = "2018/05/01"
        self.open_stragegy = False

        self.K1 = 0.2
        self.K2 = 0.3
        self.F1 = 0.4
        self.F2 = 0.5
        
        self.fired = False
        self.range_time = 7
        self.price_time = 5
        
        self.limit = 0.3/0.2 #/保证金率，17年8月22日前 0.09 后 0.2
        self.space = 1500
        self.number = 4000
        self.level = self.number * self.limit
        self.maxx = 500000 + self.level
        self.bottom = 500000 - self.level
        
        self.dayup = 0
        self.daydown = 0

        self.last_open_number = 0

        #设置价格序列
        self.close_series = []
        self.open_series = []
        self.high_series = []
        self.low_series = []
        self.time_series = []
        
        #注册策略的交易部件
        self.regist_trader()
        #注册指标模块
        self.regist_indicator()

    #注册交易信息模块
    def regist_trader(self):
        self.trader = trader.Trader()
    
    #注册所需要的指标
    def regist_indicator(self):
        self.locker = indicator.CrossLock()
    
    #返回策略的品种
    def strategy_contract(self):
        return "j"

    #返回策略逻辑的名称
    def strategy_name(self):
        return "j_cat_1min"
    
    #返回品种的级别，可选min和day
    def strategy_contract_cycle_unit(self):
        return "min"

    #返回品种的周期
    def strategy_contract_cycle(self):
        return 1
    
    #更新交易状态信息
    def update_dynamic_monitor(self):
        #更新动态权益
        self.trader.update_dynamic_equity()

        #更新动态风险度
        self.trader.update_dynamic_risk()

        #更新动态回撤率
        self.trader.update_dynamic_retreat()
    
    #开始滚动
    def strategy_rolling(self,ticker = datastruct.Ticker()):
        
        self.update_trader_data(ticker)

        self.update_dynamic_monitor()

        self.main_computation()

    def cal_range(self,N):
        High = self.history_bars('D','high',N)
        Low = self.history_bars('D','low',N)
        Close = self.history_bars('D','close',N)

        HH = max(High[:-1])
        LL = min(Low[:-1])
        LC = min(Close[:-1])
        HC = max(Close[:-1])
        range_return = max((HH-LC),(HC-LL))
        return range_return

    def before_trading(self):
        self.fired = True
        if self.dayup != 0:
            self.dayup = 0
        if self.daydown != 0:
            self.daydown = 0
        equity =  float(self.trader.dynamic_equity_vec[-1].dynamic_equity)
        self.number = int(float(equity)/200000) * self.space
        # print(self.trader.tickers[-1].date,self.trader.tickers[-1].time, "equity : ", equity)

    #主策略逻辑
    def main_computation(self):

        close = float(self.trader.tickers[-1].close)
        self.close_series.append(close)
        open_now = float(self.trader.tickers[-1].open)
        self.open_series.append(open_now)
        high = float(self.trader.tickers[-1].high)
        self.high_series.append(high)
        low = float(self.trader.tickers[-1].low)
        self.low_series.append(low)
        self.time_series.append(self.trader.tickers[-1].date + ' ' + self.trader.tickers[-1].time)

        #策略需要30根1min close，其他序列为节省时间需要相应缩短
        if len(self.close_series) > 30:
            self.close_series.pop(0)
            self.open_series.pop(0)
            self.high_series.pop(0)
            self.low_series.pop(0)
            self.time_series.pop(0)

        if self.trader.get_date() >= self.initial_day:

            if self.trader.tickers[-1].time == '21:01:00' or (self.trader.tickers[-1].time == '9:01:00' and self.trader.tickers[-2].time == '15:00:00'):
                self.before_trading()
                self.cal_range_num = self.cal_range(self.range_time)
                self.open_stragegy = True
                self.can_open = False

            elif self.trader.tickers[-1].time == '21:05:00' or (self.trader.tickers[-1].time == '9:05:00' and self.trader.tickers[-6].time == '15:00:00')  :
                self.can_open = True
            
            if self.open_stragegy == True:
                #每天记录一次开盘价
                if self.fired == True:
                    self.open_price = open_now
                    print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,self.cal_range_num)
                    self.fired = False
                
                F1 = self.F1
                F2 = self.F2
                K1 = self.K1
                K2 = self.K2

                equity =  float(self.trader.dynamic_equity_vec[-1].dynamic_equity)
                real_price = close
                buy_line = self.open_price + K1 * self.cal_range_num
                sell_line = self.open_price - K2 * self.cal_range_num
               
                current_price = talib.EMA(np.array(self.close_series),self.price_time)[-1]
               
                mutipler = 100
                self.old_level = self.level
                self.level = self.number * self.limit

                if self.old_level != self.level:
                    self.maxx = self.maxx+self.level-self.old_level
                    self.bottom = self.bottom-self.level+self.old_level
                else:
                    pass
                
                Limit = self.limit * equity
                per_margin = current_price * mutipler
                number = int(Limit / per_margin)

                if equity >= self.maxx:
                    self.bottom = self.bottom + self.level
                    self.maxx = self.maxx + self.level
                    print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'SSS')

                elif equity <= self.bottom:
                    self.bottom = self.bottom - self.level
                    self.maxx = self.maxx - self.level
                    if self.trader.market_info.direction != datastruct.Direction.Empty:
                        print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'CC')
                        if self.trader.market_info.direction  == datastruct.Direction.Short :
                            self.trader.buytocover(self.last_open_number)
                        else:   
                            self.trader.sell(self.last_open_number)
                    else:
                        pass
                else:
                    if self.dayup == 1 and self.trader.market_info.direction == datastruct.Direction.Long:
                        if real_price > self.open_price + F1 * self.cal_range_num:
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'上了解')
                            self.trader.sell(self.last_open_number)
                            self.dayup = 2
                        if real_price < self.open_price:
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'上止损')
                            self.trader.sell(self.last_open_number)
                            self.dayup = 0
                            
                    if current_price > buy_line and self.dayup == 0 and self.can_open == True:
                        if self.trader.market_info.direction == datastruct.Direction.Empty :
                            self.trader.buy(number)
                            self.last_open_number = number
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'上突', current_price)
                            self.dayup = 1
                        elif self.trader.market_info.direction  == datastruct.Direction.Short:
                            self.trader.buytocover(self.last_open_number)
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'yelloW')
                        elif self.trader.market_info.direction  == datastruct.Direction.Long:
                            self.dayup =1

                    if self.daydown ==1 and self.trader.market_info.direction == datastruct.Direction.Short:
                        if real_price < self.open_price - F2 * self.cal_range_num:
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'下了解')
                            self.trader.buytocover(self.last_open_number)
                            self.daydown = 2
                        if real_price > self.open_price - 0.1 * self.cal_range_num:
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'下止损')
                            self.trader.buytocover(self.last_open_number)
                            self.daydown = 0   

                    if current_price < sell_line and self.daydown == 0 and self.can_open == True:
                        if self.trader.market_info.direction == datastruct.Direction.Empty:
                            self.trader.sellshort(number)
                            self.last_open_number = number
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'下突')
                            self.daydown = 1
                        elif self.trader.market_info.direction  == datastruct.Direction.Long:
                            self.trader.sell(self.last_open_number)
                            print(self.trader.tickers[-1].date,self.trader.tickers[-1].time,'greeN')
                        elif self.trader.market_info.direction  == datastruct.Direction.Short:
                            self.daydown = 1




    


    

    
    




