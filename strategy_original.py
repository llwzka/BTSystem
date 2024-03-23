import quoter
import trader
import indicator
import datastruct

class Strategy_original(object):

    #输入起始资金
    def input_initial_capital(self,initial_capital):

        trader.Trader().input_initial_capital(initial_capital)
    
    #输入合约参数
    def input_contract_info(self, contract_info):
        
        self.contract_info = contract_info

        trader.Trader().input_contract_info(contract_info)

    #在策略中输入开始结束时间
    def input_begin_end_date(self,strategy_contract,begin,end): 

        self.begin_date = begin

        self.end_date = end

        self.strategy_contract_name = strategy_contract

    #更新交易段数据
    def update_trader_data(self,ticker = datastruct.Ticker()):
        #更新行情数据
        trader.Trader().input_ticker(ticker)  

    def history_bars(self,fre,data_type,N):
        #fre：分钟T 日D 月M
        test_customized_tickers = [] 
        temp = []

        #读取需要的bar数量
        if fre[:-1] == '':
            fre_n = 1
        else: 
            fre_n = int(fre[:-1])

        #处理日级别数据
        if fre[-1] == 'D':
            if trader.Trader().tickers[-1].time == "9:01:00":
                test_info =  datastruct.TestInfo(self.strategy_contract_name,'day',fre_n,self.begin_date,trader.Trader().tickers[-2].date)
            else:
                test_info =  datastruct.TestInfo(self.strategy_contract_name,'day',fre_n,self.begin_date,trader.Trader().tickers[-1].date)
        #处理分钟级别数据
        elif fre[-1] == 'T':
            test_info =  datastruct.TestInfo(self.strategy_contract_name,'min',fre_n,self.begin_date,trader.Trader().tickers[-1].date)

        quoter.Quoter().get_customized_quoter_data(test_customized_tickers, test_info)
        if data_type == "close":
            for i in range(min(len(test_customized_tickers)-1,N)):
                temp.append(float(test_customized_tickers[-(i+1)].close))
            return temp[::-1]
        if data_type == "open":
            for i in range(min(len(test_customized_tickers)-1,N)):
                temp.append(float(test_customized_tickers[-(i+1)].open))
            return temp[::-1] 
        if data_type == "low":
            for i in range(min(len(test_customized_tickers)-1,N)):
                temp.append(float(test_customized_tickers[-(i+1)].low))
            return temp[::-1]
        if data_type == "high":
            for i in range(min(len(test_customized_tickers)-1,N)):
                temp.append(float(test_customized_tickers[-(i+1)].high))
            return temp[::-1]
        

    #供输出的接口

    #输出制定的行情数据
    def output_tickers(self):
    
        trader.Trader().output_tickers()

    #打印交割单
    def output_delv_order(self):
    
        trader.Trader().output_delv_order()
    

    #输出交割单
    def output_delv_order_in_file(self):
    
        trader.Trader().output_delv_order_in_file()
    

    #打印动态权益
    def output_dynamic_equity(self):
    
        trader.Trader().output_dynamic_equity()

    #输出动态权益
    def output_dynamic_equity_in_file(self):

        trader.Trader().output_dynamic_equity_in_file()
    
    #打印动态风险度
    def output_dynamic_risk(self):
    
        trader.Trader().output_dynamic_risk()
       
    #输出动态风险度
    def output_dynamic_risk_in_file(self):
    
        trader.Trader().output_dynamic_risk_in_file() 
    
    #打印动态最大潜在回撤
    def output_dynamic_retreat(self):
    
        trader.Trader().output_dynamic_retreat()
    

    #输出动态最大潜在回撤
    def output_dynamic_retreat_in_file(self):
    
        trader.Trader().output_dynamic_retreat_in_file() 

    #输出手续费
    def output_fees_in_file(self):
    
        trader.Trader().output_fees_in_file()
    
    #输出滑点成本
    def output_slippage_in_file(self):
    
        trader.Trader().output_slippage_in_file()

    #输出总体的盈亏次数
    def output_gain_loss_times_in_file(self):
    
        trader.Trader().output_gain_loss_times_in_file() 
    
    #输出总体的盈亏值
    def output_gain_loss_in_file(self):
    
        trader.Trader().output_gain_loss_in_file()

    
    #输出profit
    def output_profit(self):
    
        print('profit: ',trader.Trader().output_profit())
    

    #输出max_retreat
    def output_max_retreat(self):
    
        print('max_retreat:',trader.Trader().output_max_retreat())

