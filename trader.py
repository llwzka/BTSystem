import datastruct
import pandas as pd

class Trader:
    #行情参数
    tickers = []

#----------------------------------------------------------------
    #交易状态信息

    #交易参数 
    market_info = datastruct.MarketInfo()
    #合约参数 
    contract_info = datastruct.ContractInfo()
    #交割单数据 datastruct.DelvOrder()
    delv_order_vec = []
    #动态权益 datastruct.DynamicEquity()
    dynamic_equity_vec = []
    #动态风险度 datastruct.DynamicRisk()
    dynamic_risk_vec = []
    #动态回撤率 datastruct.DynamicRetreat()
    dynamic_retreat_vec = []

    def input_ticker(self,ticker = datastruct.Ticker()):
        self.tickers.append(ticker)

    def input_initial_capital(self,initial_capital):
        self.market_info.initial_capital = initial_capital
    
    def input_contract_info(self,contract_info):
        self.contract_info.fees = contract_info.fees
        self.contract_info.margin_ratio = contract_info.margin_ratio
        self.contract_info.minimal_unit = contract_info.minimal_unit
        self.contract_info.multiplier = contract_info.multiplier
        self.contract_info.slippage = contract_info.slippage
        self.contract_info.strategy_name = contract_info.strategy_name
    
    def update_dynamic_equity(self):
        # print(self.market_info.direction)
        #无仓
        if self.market_info.direction == datastruct.Direction.Empty:

            if self.market_info.if_open == False and self.market_info.if_close == False:
                if not self.dynamic_equity_vec:
                    self.dynamic_equity_vec.append(datastruct.DynamicEquity(self.tickers[-1].date,self.tickers[-1].time,
                    self.market_info.initial_capital))
                else:
                    self.dynamic_equity_vec.append(datastruct.DynamicEquity(self.tickers[-1].date,self.tickers[-1].time,
                    self.dynamic_equity_vec[-1].dynamic_equity))

            else:
                if not self.dynamic_equity_vec:
                    self.dynamic_equity_vec.append(datastruct.DynamicEquity(self.tickers[-1].date,self.tickers[-1].time,
                    self.market_info.initial_capital))
                else :
                    self.dynamic_equity_vec.append(datastruct.DynamicEquity(
                        self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity
                        -self.tickers[len(self.tickers)-2].close * self.market_info.close_amount * self.contract_info.fees * self.contract_info.multiplier
                        -self.tickers[len(self.tickers)-2].close * self.market_info.open_amount * self.contract_info.fees * self.contract_info.multiplier
                        -self.market_info.close_amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage
                        -self.market_info.open_amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage
                        ))
                    # print(0,self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity,self.tickers[len(self.tickers)-2].close,self.market_info.close_amount,self.market_info.open_amount)

                    self.market_info.if_open = False
                    self.market_info.if_close = False
                    self.market_info.open_amount = 0
                    self.market_info.close_amount = 0
        #多仓
        elif self.market_info.direction == datastruct.Direction.Long:

            if self.market_info.if_open == False and self.market_info.if_close == False:
                self.dynamic_equity_vec.append(datastruct.DynamicEquity(
                    self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity
                    + (self.tickers[len(self.tickers)-1].close - self.tickers[len(self.tickers)-2].close)
                    * self.market_info.market_amount * self.contract_info.multiplier
                ))
                
            else:
                self.dynamic_equity_vec.append(datastruct.DynamicEquity(
                    self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity
                    + (self.tickers[len(self.tickers)-1].close - self.tickers[len(self.tickers)-2].close)
                    * self.market_info.market_amount * self.contract_info.multiplier
                    -self.tickers[len(self.tickers)-2].close * self.market_info.close_amount * self.contract_info.fees * self.contract_info.multiplier
                    -self.tickers[len(self.tickers)-2].close * self.market_info.open_amount * self.contract_info.fees * self.contract_info.multiplier
                    -self.market_info.close_amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage
                    -self.market_info.open_amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage
                ))
                # print(1,self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity,self.tickers[len(self.tickers)-2].close,self.market_info.close_amount,self.market_info.open_amount)


                self.market_info.if_open = False
                self.market_info.if_close = False
                self.market_info.open_amount = 0
                self.market_info.close_amount = 0

        else :
        #空仓

            if self.market_info.if_open == False and self.market_info.if_close == False :         
                self.dynamic_equity_vec.append(datastruct.DynamicEquity(
                    self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity
                    + (self.tickers[len(self.tickers)-2].close - self.tickers[len(self.tickers)-1].close)
                    * self.market_info.market_amount * self.contract_info.multiplier
                ))
            
            else :
                self.dynamic_equity_vec.append(datastruct.DynamicEquity(
                    self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity + (self.tickers[len(self.tickers)-2].close 
                    - self.tickers[len(self.tickers)-1].close) * self.market_info.market_amount * self.contract_info.multiplier
                    -self.tickers[len(self.tickers)-2].close * self.market_info.close_amount * self.contract_info.fees * self.contract_info.multiplier
                    -self.tickers[len(self.tickers)-2].close * self.market_info.open_amount * self.contract_info.fees * self.contract_info.multiplier
                    -self.market_info.close_amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage
                    -self.market_info.open_amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage))
                # print(2,self.tickers[-1].date,self.tickers[-1].time,self.dynamic_equity_vec[-1].dynamic_equity,self.tickers[len(self.tickers)-2].close,self.market_info.close_amount,self.market_info.open_amount)

                self.market_info.if_open = False
                self.market_info.if_close = False
                self.market_info.open_amount = 0
                self.market_info.close_amount = 0


    def update_dynamic_risk(self):

        self.dynamic_risk_vec.append(datastruct.DynamicRisk(
            self.tickers[-1].date,self.tickers[-1].time,self.market_info.market_amount * self.tickers[-1].close
            * self.contract_info.margin_ratio * self.contract_info.multiplier 
            / self.dynamic_equity_vec[-1].dynamic_equity))


    def update_dynamic_retreat(self):

        if self.dynamic_equity_vec[-1].dynamic_equity > self.market_info.highest_interest :

            self.market_info.highest_interest = self.dynamic_equity_vec[-1].dynamic_equity
            self.dynamic_retreat_vec.append(datastruct.DynamicRetreat(
                self.tickers[-1].date,self.tickers[-1].time,0))

        else :

            self.dynamic_retreat_vec.append(datastruct.DynamicRetreat(
                self.tickers[-1].date,self.tickers[-1].time,(self.market_info.highest_interest 
                - self.dynamic_equity_vec[-1].dynamic_equity) / self.market_info.highest_interest))

 

#--------------------------------------------------------------------#
#每一步供策略或者指标读取交易参数

    def close(self,counter = None):
        if counter == None:
            return self.tickers[-1].close
        if counter >= len(self.tickers):
            return self.tickers[0].close
        else:
            return self.tickers[len(self.tickers)-1-counter].close

    def open(self, counter = None):
        if counter == None:
            return self.tickers[-1].open
        if counter >= len(self.tickers):
            return self.tickers[0].open
        else:
            return self.tickers[len(self.tickers)-1-counter].open
    
    def high(self,counter = None):
        if counter == None:
            return self.tickers[-1].high    
        if counter >= len(self.tickers):
            return self.tickers[0].high
        else:
            return self.tickers[len(self.tickers)-1-counter].high

    def low(self,counter = None):
        if counter == None:
            return self.tickers[-1].low   
        if counter >= len(self.tickers):
            return self.tickers[0].low
        else:
            return self.tickers[len(self.tickers)-1-counter].low

    def get_date(self):
        return self.tickers[-1].date

    def get_time(self):
        return self.tickers[-1].time

    def market_direction(self):
        return self.market_info.direction

    def open_price(self):
        return self.market_info.open_price

    def margin_ratio(self):
        return self.contract_info.margin_ratio

    def multiplier(self):
        return self.contract_info.multiplier

    def minimal_unit(self):
        return self.contract_info.minimal_unit

    def market_amount(self):
        return self.market_info.market_amount

    def current_capital(self):
        return self.dynamic_equity_vec[-1].dynamic_equity

    def current_retreat(self):
        return self.dynamic_retreat_vec[-1].dynamic_retreat


#---------------------------------------------------------------------#
#交易指令

    def buytocover(self,input_number):

        if self.market_info.direction == datastruct.Direction.Long:
            print("wrong order!")
        elif ((self.market_info.direction == datastruct.Direction.Short) or (self.market_info.direction == datastruct.Direction.Empty)) and (self.market_info.market_amount < input_number):
            print("wrong order!")
        elif (self.market_info.direction == datastruct.Direction.Empty) and (input_number == 0):
            return
        else:
        
            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"buy","close",input_number,self.tickers[-1].close))
    
            if self.market_info.market_amount == input_number:
                self.market_info.direction = datastruct.Direction.Empty
            else:
                self.market_info.direction = datastruct.Direction.Short

            self.market_info.market_amount -= input_number

            #记录开仓信息
            self.market_info.if_close = True
            self.market_info.close_amount = input_number
        
    

    def sell(self, input_number):

        if self.market_info.direction == datastruct.Direction.Short:
            print("wrong order!")
        elif ((self.market_info.direction == datastruct.Direction.Long) or (self.market_info.direction == datastruct.Direction.Empty)) and (self.market_info.market_amount < input_number):
            print("wrong order!")
        elif (self.market_info.direction == datastruct.Direction.Empty) and (input_number == 0):
            return
        else:
        
            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"sell","close",input_number,self.tickers[-1].close))
    
            if self.market_info.market_amount == input_number:
                self.market_info.direction = datastruct.Direction.Empty
            else:
                self.market_info.direction = datastruct.Direction.Long

            self.market_info.market_amount -= input_number

            #记录开仓信息
            self.market_info.if_close = True
            self.market_info.close_amount = input_number

    def buy(self,input_number):

        if self.market_info.direction == datastruct.Direction.Empty:
            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"buy","open",input_number,self.tickers[-1].close))

            self.market_info.direction = datastruct.Direction.Long
            self.market_info.open_price = self.tickers[-1].close
            self.market_info.market_amount = input_number

            #记录开仓信息
            self.market_info.if_open = True
            self.market_info.open_amount = input_number
        

        elif self.market_info.direction == datastruct.Direction.Long:
        
            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"buy","open",input_number,self.tickers[-1].close))

            self.market_info.open_price = (self.market_info.open_price*self.market_info.market_amount + self.tickers[-1].close*input_number)/(self.market_info.market_amount+input_number)
            self.market_info.market_amount += input_number

            #记录开仓信息
            self.market_info.if_open = True
            self.market_info.open_amount = input_number


        else:
            self.buytocover(self.market_info.market_amount)

            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"buy","open",input_number,self.tickers[-1].close))


            self.market_info.direction = datastruct.Direction.Long
            self.market_info.open_price = self.tickers[-1].close
            self.market_info.market_amount = input_number

            #记录开仓信息
            self.market_info.if_open = True
            self.market_info.open_amount = input_number


    def sellshort(self,input_number):

        if self.market_info.direction == datastruct.Direction.Empty:
            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"sell","open",input_number,self.tickers[-1].close))

            self.market_info.direction = datastruct.Direction.Short
            self.market_info.open_price = self.tickers[-1].close
            self.market_info.market_amount = input_number

            #记录开仓信息
            self.market_info.if_open = True
            self.market_info.open_amount = input_number
        

        elif self.market_info.direction == datastruct.Direction.Short:
        
            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"sell","open",input_number,self.tickers[-1].close))

            self.market_info.open_price = (self.market_info.open_price*self.market_info.market_amount + self.tickers[-1].close*input_number)/(self.market_info.market_amount+input_number)
            self.market_info.market_amount += input_number

            #记录开仓信息
            self.market_info.if_open = True
            self.market_info.open_amount = input_number


        else:
            self.sell(self.market_info.market_amount)

            self.delv_order_vec.append(datastruct.DelvOrder(self.tickers[-1].date,self.tickers[-1].time,"sell","open",input_number,self.tickers[-1].close))


            self.market_info.direction = datastruct.Direction.Short
            self.market_info.open_price = self.tickers[-1].close
            self.market_info.market_amount = input_number

            #记录开仓信息
            self.market_info.if_open = True
            self.market_info.open_amount = input_number

#----------------------------------------------------------------------------------------------------------------------
#输出全部数据接口

    #输出K线数据
    def output_tickers(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_quote_date.csv"
        total_tickers = {}

        for i in range(len(self.tickers)):
            total_tickers[i] = [self.tickers[i].date,self.tickers[i].time,self.tickers[i].open,self.tickers[i].high,self.tickers[i].low,self.tickers[i].close,self.tickers[i].vol]

        pd.DataFrame(total_tickers).T.to_csv(output_filename)
    
    #打印交割单
    def output_delv_order(self):
        print("deliver_order")
        for delv_order in self.delv_order_vec:
            print(delv_order.date,',',delv_order.time,',',delv_order.buy_or_sell,',',delv_order.open_or_close,',',delv_order.amount,',',delv_order.price)
    
    #输出交割单
    def output_delv_order_in_file(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_diliver_order.csv"
        delv_order = {}

        for i in range(len(self.delv_order_vec)):
            delv_order[i] = [self.delv_order_vec[i].date,self.delv_order_vec[i].time,self.delv_order_vec[i].buy_or_sell,self.delv_order_vec[i].open_or_close,self.delv_order_vec[i].amount,self.delv_order_vec[i].price]

        pd.DataFrame(delv_order).T.to_csv(output_filename)            

    #打印动态权益
    def output_dynamic_equity(self):

        print("dynamic_equity")
        for dynamic_equity in self.dynamic_equity_vec:

            print(dynamic_equity.date,',',dynamic_equity.time,',',dynamic_equity.dynamic_equity)
             


    #输出动态权益
    def output_dynamic_equity_in_file(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_dynamic_equity.csv"
        dynamic_equity = {}

        for i in range(len(self.dynamic_equity_vec)):
            dynamic_equity[i] = [self.dynamic_equity_vec[i].date,self.dynamic_equity_vec[i].time,self.dynamic_equity_vec[i].dynamic_equity]

        pd.DataFrame(dynamic_equity).T.to_csv(output_filename)
        
    #打印动态风险度
    def output_dynamic_risk(self):
        print("dynamic_risk")
        for dynamic_risk in self.dynamic_risk_vec:
            print(dynamic_risk.date,',',dynamic_risk.time,',',dynamic_risk.dynamic_risk)
        
    

    #输出动态风险度
    def output_dynamic_risk_in_file(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_dynamic_risk.csv"
        dynamic_risk = {}

        for i in range(len(self.dynamic_risk_vec)):
            dynamic_risk[i] = [self.dynamic_risk_vec[i].date,self.dynamic_risk_vec[i].time,self.dynamic_risk_vec[i].dynamic_risk]

        pd.DataFrame(dynamic_risk).T.to_csv(output_filename)
    
    #打印动态最大潜在回撤率
    def output_dynamic_retreat(self):
        print("dynamic_retreat")
        for dynamic_retreat in self.dynamic_retreat_vec:
            print(dynamic_retreat.date,',',dynamic_retreat.time,',',dynamic_retreat.dynamic_retreat)

    #输出动态最大潜在回撤率
    def output_dynamic_retreat_in_file(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_dynamic_retreat.csv"
        dynamic_retreat = {}

        for i in range(len(self.dynamic_retreat_vec)):
            dynamic_retreat[i] = [self.dynamic_retreat_vec[i].date,self.dynamic_retreat_vec[i].time,self.dynamic_retreat_vec[i].dynamic_retreat]

        pd.DataFrame(dynamic_retreat).T.to_csv(output_filename)
    
    #输出所使用的手续费
    def output_fees_in_file(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_fees.csv"
        fees_sum = 0
        total = {}

        for i in range(len(self.delv_order_vec)):
            fees = self.delv_order_vec[i].amount * self.delv_order_vec[i].price * self.contract_info.fees * self.contract_info.multiplier
            fees_sum += fees
            total[i] = [self.delv_order_vec[i].date,self.delv_order_vec[i].time,fees,fees_sum]
        
        pd.DataFrame(total).T.to_csv(output_filename)

    #输出总共产生的滑点成本
    def output_slippage_in_file(self):
        output_filename = "output/" + self.contract_info.strategy_name + "_slippage.csv"
        slippage_sum = 0
        total = {}

        for i in range(len(self.delv_order_vec)):
            slippage = self.delv_order_vec[i].amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage
            slippage_sum += slippage
            total[i] = [self.delv_order_vec[i].date,self.delv_order_vec[i].time,slippage,slippage_sum]
        
        pd.DataFrame(total).T.to_csv(output_filename)

    #输出总体的盈亏次数
    def output_gain_loss_times_in_file(self):

        output_filename = "output/" + self.contract_info.strategy_name + "_gain_loss_times.csv"

        gain_counter = 0
        loss_counter = 0
        total={}

        for i in range(len(self.delv_order_vec)):

            if self.delv_order_vec[i].open_or_close == "close":
            
                if self.delv_order_vec[i].buy_or_sell == "sell":
                
                    if self.delv_order_vec[i].price - self.delv_order_vec[i-1].price > 0:
                        gain_counter = gain_counter + 1
                    else:
                        loss_counter = loss_counter + 1
                
                else:
            
                    if self.delv_order_vec[i-1].price - self.delv_order_vec[i].price > 0:
                        gain_counter = gain_counter + 1
                    else:
                        loss_counter = loss_counter + 1

        total = {'gain_counter':[gain_counter],'loss_counter':[loss_counter]}
        # print(total)
        pd.DataFrame(total).to_csv(output_filename)

    #输出盈亏比率
    # def output_gain_loss_ratio_in_file(self):

    #     output_filename = "output/" + self.contract_info.strategy_name + "_gain_loss_ratios.csv"
        
    #     total={}

    #     for i in range(len(self.delv_order_vec)):

    #         if self.delv_order_vec[i].open_or_close == "close":
            
    #             if self.delv_order_vec[i].buy_or_sell == "sell":
                
    #                 if self.delv_order_vec[i].price - self.delv_order_vec[i-1].price > 0:
    #                     gain_counter = gain_counter + 1
    #                 else:
    #                     loss_counter = loss_counter + 1
                
    #             else:
            
    #                 if self.delv_order_vec[i-1].price - self.delv_order_vec[i].price > 0:
    #                     gain_counter = gain_counter + 1
    #                 else:
    #                     loss_counter = loss_counter + 1



    #输出总盈利和总亏损
    def output_gain_loss_in_file(self):

        output_filename = "output/" + self.contract_info.strategy_name + "_gain_loss.csv"

        gain = 0
        loss = 0
        total={}

        for i in range(len(self.delv_order_vec)):
        
            if self.delv_order_vec[i].open_or_close == "close":

                fee_cost = (self.delv_order_vec[i].price * self.delv_order_vec[i].amount + self.delv_order_vec[i-1].price * self.delv_order_vec[i-1].amount) * self.contract_info.fees * self.contract_info.multiplier
                slippage_cost = self.delv_order_vec[i].amount * self.contract_info.minimal_unit * self.contract_info.multiplier * self.contract_info.slippage * 2
                extra_cost = fee_cost + slippage_cost

                if self.delv_order_vec[i].buy_or_sell == "sell":
                
                    if self.delv_order_vec[i].price - self.delv_order_vec[i-1].price > 0:
                        gain += (self.delv_order_vec[i].price - self.delv_order_vec[i-1].price) * self.contract_info.multiplier * self.delv_order_vec[i].amount - extra_cost
                    else:
                        loss += (self.delv_order_vec[i].price - self.delv_order_vec[i-1].price) * self.contract_info.multiplier * self.delv_order_vec[i].amount - extra_cost
                
                else:
                
                    if self.delv_order_vec[i-1].price - self.delv_order_vec[i].price > 0:
                        gain += (self.delv_order_vec[i-1].price - self.delv_order_vec[i].price) * self.contract_info.multiplier * self.delv_order_vec[i].amount - extra_cost
                    else:
                        loss += (self.delv_order_vec[i-1].price - self.delv_order_vec[i].price) * self.contract_info.multiplier * self.delv_order_vec[i].amount - extra_cost

        total = {'gain':[gain],'loss':[loss]}
        pd.DataFrame(total).to_csv(output_filename)

    #输出最后的利润
    def output_profit(self):

        #求最后的总权益
        final_dynamic_equity = self.dynamic_equity_vec[-1].dynamic_equity

        return final_dynamic_equity / self.market_info.initial_capital 

    #输出最大回撤
    def output_max_retreat(self):
    
        #求最大的潜在回撤值
        max_retreat = 0

        for dynamic_retreat in self.dynamic_retreat_vec:
        
            if dynamic_retreat.dynamic_retreat > max_retreat:
                max_retreat = dynamic_retreat.dynamic_retreat
        

        return max_retreat


##################################清空已有数据######################
    def delete(self):
        #行情参数
        if self.tickers:
            del self.tickers[:]
            del self.delv_order_vec[:]
            del self.dynamic_equity_vec[:]
            del self.dynamic_risk_vec[:]
            del self.dynamic_retreat_vec[:]

            #初始化market_info中的各项参数
            self.market_info.direction = datastruct.Direction.Empty
            self.market_info.open_price = 0 
            self.market_info.market_amount = int(0)
            self.market_info.initial_capital = 0
            self.market_info.highest_interest = 0
            self.market_info.if_open = False
            self.market_info.open_amount = int(0)
            self.market_info.if_close = False
            self.market_info.close_amount = int(0)

            #初始化contract_info中的各项参数
            self.contract_info.strategy_name = ' '
            self.contract_info.margin_ratio = 0
            self.contract_info.multiplier = 0
            self.contract_info.minimal_unit = 0
            self.contract_info.fees = 0
            self.contract_info.slippage = 0


    