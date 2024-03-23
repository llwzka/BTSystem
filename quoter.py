import datastruct
import pandas as pd
import datetime

class Quoter:
    tickers = {} 
    #输入各个合约的合约参数
    def __init__(self,path = None):
        if path:
            self.contract_info = datastruct.JsonConf().load(path)
        
        # print(self.contract_info)
        
    #输入各个合约的行情数据
    def read_quoter_data(self,contract_name,filename):
        if contract_name in self.tickers:
            print("该合约已经注册过了： ",contract_name)
        else:
            self.ticker = datastruct.Ticker()

            filedata = pd.read_csv(filename) 

            self.ticker.date = filedata['Date']
            self.ticker.time = filedata['Time']
            self.ticker.open = filedata['Open']
            self.ticker.high = filedata['High']
            self.ticker.low = filedata['Low']
            self.ticker.close = filedata['Close']
            self.ticker.vol = filedata['Volume']

            self.tickers[contract_name] = self.ticker
            # print(self.tickers['ru'].close) 

    #读取各个品种的合约参数
    def read_contract_info(self,contract_name,strategy_name):
        info = self.contract_info[contract_name]
        return datastruct.ContractInfo(strategy_name,
                             info["margin_ratio"],
                             info["contract_multiplier"],
                             info["contract_minimal_unit"],
                             info["fees"],
                             info["slippage"])

    #根据策略的要求返回相应的策略定制分钟行情
    def get_customized_quoter_data(self,customized_tickers,test_info) :

        #取得测试的日期区间，如果区间不存在返回空指针
        test_date_ptr = self.get_test_date(test_info)

        if test_date_ptr == None :
            return

        #取得测试周期内的ticker
        test_tickers = datastruct.Ticker()
        self.get_test_tickers(test_tickers, test_date_ptr, test_info.contract_name)


        #根据回测的时间范围要级别取得相应的行情数据
        if test_info.contract_cycle_unit == "min" :
            self.get_customized_tickers_min(customized_tickers, test_tickers, test_info)
        elif test_info.contract_cycle_unit == "day" :
            self.get_customized_tickers_day(customized_tickers, test_tickers, test_info)
    
    #在原先函数的基础上有所更改
    def get_test_date(self,test_info):

        #控制台要求的时间范围
        #设置每日交易开始和结束时间
        ct_begin_date = pd.to_datetime(test_info.begin_date + ' 21:01:00')
        ct_end_date = pd.to_datetime(test_info.end_date + ' 15:00:00')

        #原始行情数据拥有的时间范围
        tk_begin_date = pd.to_datetime(self.tickers[test_info.contract_name].date[0])
        tk_end_date = pd.to_datetime(self.tickers[test_info.contract_name].date[len(self.tickers[test_info.contract_name].date)-1])

        #实际的测试时间范围
        if ct_end_date < tk_begin_date and ct_begin_date > tk_end_date :

            print(test_info.contract_name,"'s quoter_date is empty")
            return {}

        else :
            if ct_begin_date > tk_begin_date : 
                test_begin_date = ct_begin_date
            else:
                test_begin_date = tk_begin_date

            if ct_end_date > tk_end_date:
                test_end_date = tk_end_date
            else:
                test_end_date = ct_end_date

        return [test_begin_date,test_end_date]


    #取得测试范围内的ticker
    def get_test_tickers(self, test_tickers, test_date_ptr, contract_name) :
        temp_ticker = self.tickers[contract_name]
        test_begin_date = test_date_ptr[0]
        test_end_date = test_date_ptr[1]

        temp_ticker.index = pd.to_datetime(temp_ticker.date +' '+ temp_ticker.time)

        test_tickers.date = temp_ticker.date[test_begin_date <= temp_ticker.index]
        test_tickers.date = test_tickers.date[temp_ticker.index <= test_end_date]
        test_tickers.time = temp_ticker.time[test_begin_date <= temp_ticker.index]
        test_tickers.time = test_tickers.time[temp_ticker.index <= test_end_date]
        test_tickers.open = temp_ticker.open[test_begin_date <= temp_ticker.index]
        test_tickers.open = test_tickers.open[temp_ticker.index <= test_end_date]
        test_tickers.high = temp_ticker.high[test_begin_date <= temp_ticker.index]
        test_tickers.high = test_tickers.high[temp_ticker.index <= test_end_date]
        test_tickers.low = temp_ticker.low[test_begin_date <= temp_ticker.index]
        test_tickers.low = test_tickers.low[temp_ticker.index <= test_end_date]
        test_tickers.close = temp_ticker.close[test_begin_date <= temp_ticker.index]
        test_tickers.close = test_tickers.close[temp_ticker.index <= test_end_date]
        test_tickers.vol = temp_ticker.vol[test_begin_date <= temp_ticker.index]
        test_tickers.vol = test_tickers.vol[temp_ticker.index <= test_end_date]


    #根据回测的时间范围要级别取得相应的分钟行情数据
    def get_customized_tickers_min(self, customized_tickers, test_tickers, test_info) : #test_tickers的每个元素都是series类型
        start_time = datetime.datetime.strptime(test_tickers.date.values[0]+' '+test_tickers.time.values[0], "%Y/%m/%d %H:%M:%S")
        start_time = start_time + datetime.timedelta(minutes = -1)
        end_time = start_time + datetime.timedelta(minutes = test_info.contract_cycle)
        temp_tickers = []
        
        for i in range(len(test_tickers.time)):
            ticker = datastruct.Ticker()
            ticker.time,ticker.date,ticker.close,ticker.high,ticker.low,ticker.open,ticker.vol = test_tickers.time.values[i],test_tickers.date.values[i],test_tickers.close.values[i],test_tickers.high.values[i],test_tickers.low.values[i],test_tickers.open.values[i],test_tickers.vol.values[i]
            ticker_timenow = datetime.datetime.strptime(test_tickers.date.values[i]+' '+test_tickers.time.values[i], "%Y/%m/%d %H:%M:%S")
            if ((start_time < end_time) and (ticker_timenow > end_time)) or ((start_time < end_time) and (ticker_timenow < start_time)) or ((start_time > end_time) and (ticker_timenow < start_time) and (ticker_timenow > end_time)):
                start_time = ticker_timenow + datetime.timedelta(minutes = -1)
                end_time = start_time + datetime.timedelta(minutes = test_info.contract_cycle)
                customized_tickers.append(self.get_cycle_ticker(temp_tickers))
                temp_tickers = []
            
            temp_tickers.append(ticker)
        
        customized_tickers.append(self.get_cycle_ticker(temp_tickers))

    #根据回测的时间范围要级别取得相应的日行情数据
    def get_customized_tickers_day(self, customized_tickers, test_tickers, test_info):
        temp_tickers = []
        counter = 1

        for i in range(len(test_tickers.time)):
            ticker = datastruct.Ticker()
            ticker.time,ticker.date,ticker.close,ticker.high,ticker.low,ticker.open,ticker.vol = test_tickers.time.values[i],test_tickers.date.values[i],test_tickers.close.values[i],test_tickers.high.values[i],test_tickers.low.values[i],test_tickers.open.values[i],test_tickers.vol.values[i]
            temp_tickers.append(ticker)

            if temp_tickers and ticker.time == "15:00:00":
                if counter < test_info.contract_cycle :
                    counter = counter + 1

                else:
                    customized_tickers.append(self.get_cycle_ticker(temp_tickers))
                    temp_tickers = []
                    counter = 1

    #输入周期内所有的一分钟K线，输出整合后的定制周期后的ticker
    def get_cycle_ticker(self, temp_tickers):

        open = temp_tickers[0].open
        close = temp_tickers[-1].close
        high = temp_tickers[0].high
        low = temp_tickers[0].low

        vol = 0
        for ticker in temp_tickers :

            vol = ticker.vol + vol

            if ticker.high > high:
                high = ticker.high

            if ticker.low < low:
                low = ticker.low

        return datastruct.Ticker(temp_tickers[-1].date, temp_tickers[-1].time, open, high, low, close, vol)
