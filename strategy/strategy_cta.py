from quoter import trader, indicator, datastruct
import strategy_original


class Strategy(strategy_original.Strategy_original): 
    def __init__(self):
        #设置
        self.initial_day = "2017/07/01"
        #设置ema短均线周期
        self.ema_window_short  = 6
        #设置长均线周期
        self.ema_window_long = 66
        #设置每次新入场手数比例
        self.initial_percent = 0.005

        #注册策略的交易部件
        self.regist_trader()
        #注册指标模块
        self.regist_indicator()
    
    def read_initial_day(self,day):

        self.initial_day = day

    #注册交易信息模块
    def regist_trader(self):
        self.trader = trader.Trader()
    
    #注册所需要的指标
    def regist_indicator(self):
        self.ema_short = indicator.Ema(self.ema_window_short)
        self.ema_long = indicator.Ema(self.ema_window_long)
        self.ema_locker = indicator.CrossLock()
    
    #返回策略的品种
    def strategy_contract(self):
        return "ru"

    #返回策略逻辑的名称
    def strategy_name(self):
        return "ru_cta_1min"
    
    #返回品种的级别
    def strategy_contract_cycle_unit(self):
        return "min"

    #返回品种的周期
    def strategy_contract_cycle(self):
        return 1

    #开始滚动
    def strategy_rolling(self, ticker = datastruct.Ticker()):
        
        self.update_trader_data(ticker)

        self.update_dynamic_monitor()

        self.main_computation()

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

        close = self.trader.tickers[-1].close
        ema_short = self.ema_short.update(close)
        ema_long = self.ema_long.update(close)

#--------------------------------------------------------------------------------------
#双均线

        if self.trader.get_date() >= self.initial_day:
            if self.ema_locker.if_cross_over(ema_short,ema_long):
                amount = (10000000 * self.initial_percent) // (int(self.trader.close()) * self.contract_info.multiplier * self.contract_info.margin_ratio)
                self.trader.buy(amount)
                
            

            elif self.ema_locker.if_cross_under(ema_short,ema_long):
                amount = (10000000 * self.initial_percent) // (int(self.trader.close()) * self.contract_info.multiplier * self.contract_info.margin_ratio)
                self.trader.sellshort(amount)
                

    

    
    




