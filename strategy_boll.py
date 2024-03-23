import trader
import indicator
import datastruct
import pandas as pd
import time
import numpy as np
import strategy_original


class Strategy(strategy_original.Strategy_original):
    
    def __init__(self):
        #设置
        self.initial_day = "2018/07/11"
        #设置趋势定义比例
        self.trend_percent = 0.05
        #设置每次新入场手数比例
        self.initial_percent = 0.005
        #设置最高限仓比例
        self.max_percent = 0.01


        #策略内部调用的参数

        #上一次开仓价格
        self.last_entry_price = -1
        #最新的lost值
        self.current_lost = 0
        #趋势完成后的起始开仓数
        self.initial_amount = 1
        #限制仓位开仓数
        self.lim_amount = 1
        #最终开仓数
        self.amount = 1 
        #是否开始入场
        self.if_do = False

        #指标参数

        #设置bollinger周期
        self.bollinger_window = 20 
        #设置var周期
        self.var_window = 20
        #设置std周期
        self.std_window = 20 
        #设置ma均线周期
        self.ma_window = 20 

        #设置价格序列
        self.close_series = []

        #设置标准差的倍数
        self.std_multi = 2
        #注册指标
        self.time_used = 0
        
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
        return "ru"

    #返回策略逻辑的名称
    def strategy_name(self):
        return "ru_boll_3min"
    
    #返回品种的级别，可选min和day
    def strategy_contract_cycle_unit(self):
        return "min"

    #返回品种的周期
    def strategy_contract_cycle(self):
        return 3

    #输入起始资金
    def input_initial_capital(self,initial_capital):

        self.trader.input_initial_capital(initial_capital)
    
    #输入合约参数
    def input_contract_info(self, contract_info):
        self.contract_info = contract_info
        self.trader.input_contract_info(contract_info)

    #开始滚动
    def strategy_rolling(self,ticker = datastruct.Ticker()):
        
        self.update_trader_data(ticker)

        self.update_dynamic_monitor()

        self.main_computation()

    #更新交易段数据
    def update_trader_data(self,ticker = datastruct.Ticker()):
        #更新行情数据
        self.trader.input_ticker(ticker)  

    #更新交易状态信息
    def update_dynamic_monitor(self):
        #更新动态权益
        self.trader.update_dynamic_equity()

        #更新动态风险度
        self.trader.update_dynamic_risk()

        #更新动态回撤率
        self.trader.update_dynamic_retreat()

    #主策略逻辑
    def main_computation(self):
        
        close = float(self.trader.tickers[-1].close)
        self.close_series.append(close)

        bollingerband_up = indicator.Bollinger().Up(self.close_series,self.bollinger_window,self.std_multi)
        bollingerband_down = indicator.Bollinger().Down(self.close_series,self.bollinger_window,self.std_multi)
        # std_data = np.std(self.close_series[-self.bollinger_window:],ddof = 1)
        # mean_data = np.mean(self.close_series[-self.bollinger_window:])

#--------------------------------------------------------------------------------------
#布林带震荡策略

        if self.trader.get_date() >= self.initial_day:
            # print(self.trader.get_date(),self.trader.get_time(),bollingerband_up,bollingerband_down,close,mean_data,std_data)
            if self.locker.if_cross_under(close,bollingerband_up):
                amount = (10000000 * self.initial_percent) // (self.trader.close() * self.contract_info.multiplier * self.contract_info.margin_ratio)
                self.trader.sellshort(amount)
                # print(1,self.trader.get_date(),ema_short,close,ema_long)
                
            

            elif self.locker.if_cross_over(close,bollingerband_down):
                amount = (10000000 * self.initial_percent) // (self.trader.close() * self.contract_info.multiplier * self.contract_info.margin_ratio)
                self.trader.buy(amount)
                # print(2,self.trader.get_date(),ema_short,close,ema_long)
                

#---------------------------------------------------------------------------
#供输出的接口

    #输出制定的行情数据
    def output_tickers(self):
    
        self.trader.output_tickers()

    #打印交割单
    def output_delv_order(self):
    
        self.trader.output_delv_order()
    

    #输出交割单
    def output_delv_order_in_file(self):
    
        self.trader.output_delv_order_in_file()
    
    

    #打印动态权益
    def output_dynamic_equity(self):
    
        self.trader.output_dynamic_equity()

    #输出动态权益
    def output_dynamic_equity_in_file(self):

        self.trader.output_dynamic_equity_in_file()
    
    #打印动态风险度
    def output_dynamic_risk(self):
    
        self.trader.output_dynamic_risk()
       
    #输出动态风险度
    def output_dynamic_risk_in_file(self):
    
        self.trader.output_dynamic_risk_in_file() 
    
    #打印动态最大潜在回撤
    def output_dynamic_retreat(self):
    
        self.trader.output_dynamic_retreat()
    

    #输出动态最大潜在回撤
    def output_dynamic_retreat_in_file(self):
    
        self.trader.output_dynamic_retreat_in_file() 

    #输出手续费
    def output_fees_in_file(self):
    
        self.trader.output_fees_in_file()
    
    #输出滑点成本
    def output_slippage_in_file(self):
    
        self.trader.output_slippage_in_file()

    #输出总体的盈亏次数
    def output_gain_loss_times_in_file(self):
    
        self.trader.output_gain_loss_times_in_file()
    
    #输出总体的盈亏值
    def output_gain_loss_in_file(self):
    
        self.trader.output_gain_loss_in_file()

    
    #输出profit
    def output_profit(self):
    
        print('profit: ',self.trader.output_profit())
    

    #输出max_retreat
    def output_max_retreat(self):
    
        print('max_retreat:',self.trader.output_max_retreat())
    


    

    
    




