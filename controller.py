import quoter
import datastruct
import trader
import pandas as pd
import datetime

class Controller:
    #策略向量为字典，Key为品种名，具体策略保存在Key下，为list
    strategies_vec ={}
    begin_date = ' '
    end_date = ' '
    initial_capital = 0
    contract_info = datastruct.ContractInfo()
    
    #读取合约参数
    def __init__(self,path = None):
        self.path = path
        #注册报价管理器,将各个品种的合约参数输入给报价管理器
        self.quoter = quoter.Quoter(path)

    #读取单个合约的行情数据 
    def read_quoter_data(self,contract_name, filename):
        self.quoter.read_quoter_data(contract_name, filename)
    
    #把main函数注册的策略实例挂载到controller里
    def regist_strategy(self,strategy):
        flag = 0
        if strategy.strategy_contract() in self.strategies_vec:
            for st in self.strategies_vec[strategy.strategy_contract()]:
                if strategy.strategy_name() == st.strategy_name() :
                    print("该策略已经注册过了：",strategy.strategy_name())
                    flag = 1

        if flag == 0:
            if strategy.strategy_contract() not in self.strategies_vec:
                self.strategies_vec[strategy.strategy_contract()] = [strategy]
            else:
                self.strategies_vec[strategy.strategy_contract()].append(strategy)

    #读取初始资本金额 
    def get_initial_capital(self,initial_capital):
        self.initial_capital = initial_capital
    
    #读取回测开始结束时间
    def read_start_end_date(self,begin_date,end_date):
        self.begin_date = begin_date
        self.end_date = end_date

    
    #滚动策略
    def start(self):

        if self.begin_date == ' ' and self.end_date == ' ' :

            print("the test date has not been set")
        
        else :
            #先对品种进行循环，然后再对策略进行循环
            for sc in self.strategies_vec :

                for st in self.strategies_vec[sc] :
                    
                    #删除trader中保存的信息，例如交割单、权益等
                    trader.Trader().delete()

                    self.contract_info = quoter.Quoter(self.path).read_contract_info(st.strategy_contract(), st.strategy_name())

                    #打印策略名称
                    print(st.strategy_name())

                    #输入起始资金
                    st.input_initial_capital(self.initial_capital)

                    #输入合约参数
                    st.input_contract_info(self.contract_info)
    
                    #注册策略所定制的行情vector
                    test_customized_tickers = [] 

                    #生成策略需要的测试信息
                    test_info = datastruct.TestInfo(st.strategy_contract(),st.strategy_contract_cycle_unit(),st.strategy_contract_cycle(),self.begin_date,self.end_date)
                    
                    #将所需策略信息传给strategy
                    st.input_begin_end_date(st.strategy_contract(),self.begin_date,self.end_date)

                    quoter.Quoter(self.path).get_customized_quoter_data(test_customized_tickers, test_info) 

                    if not test_customized_tickers :

                        continue

                    for counter in range(len(test_customized_tickers)) :
                        st.strategy_rolling(test_customized_tickers[counter])
                    
                    
                    #这里设置需要输出什么样的数据

                    st.output_dynamic_equity_in_file()
                    # st.output_dynamic_equity()
                    # st.output_dynamic_risk_in_file()
                    # st.output_dynamic_retreat_in_file()
                    # st.output_dynamic_retreat()
                    # st.output_tickers()
                    st.output_delv_order_in_file()
                    # st.output_fees_in_file()
                    # st.output_slippage_in_file()
                    # st.output_gain_loss_times_in_file()
                    # st.output_gain_loss_in_file()
                    # st.output_profit()
                    # st.output_max_retreat()
    
    #计算并输出策略组合的总体动态权益
    def total_dynamic_equity(self):
        #记录策略的数量
        count = 0

        #先对品种进行循环，然后再对策略进行循环
        for sc in self.strategies_vec :
            for st in self.strategies_vec[sc] :
                count = count + 1
                #读取不同策略的动态权益
                temp_data = pd.read_csv("output/" + st.strategy_name() + "_dynamic_equity.csv")
                #设置时间戳
                temp_data.index = pd.to_datetime(temp_data['0'] + ' ' + temp_data['1'])
                #去掉多余的列
                temp_data.drop(['Unnamed: 0','0','1'],axis = 1,inplace = True)
                #动态权益列改名
                temp_data = temp_data.rename(columns={'2':'dynamic_equity'})
                #设置回测时间，按分钟输出当前时刻的动态权益
                idx = pd.date_range(start = self.begin_date,end = self.end_date + " 15:00:00",freq = 'T')
                temp_data = temp_data.reindex(idx)
                temp_data.iloc[0,0] = self.initial_capital
                #向前填充
                temp_data.fillna(method='ffill', inplace=True)
                if count == 1:
                    total_data = temp_data
                else:
                    total_data['dynamic_equity'] += temp_data['dynamic_equity']
        
        #计算总体动态权益
        total_data['dynamic_equity'] = total_data['dynamic_equity']/count
        # print(total_data)

        #将总体动态权益输出到文件
        total_data.to_csv("output/" + "total_dynamic_equity.csv")




        

                    
                    

 

