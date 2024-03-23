import datastruct
import pandas as pd
import numpy as np

class Ema:
    n = 0   
    def __init__(self,window):
        self.alpha = 2/(1+window)      
    
    def fit(self, value):
        if self.n == 0 :
            self.ema = value
            self.n = self.n + 1
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema 
            self.n = self.n + 1


    def get(self,value):
        return self.ema

    def update(self,value):
        self.fit(value)
        return self.get(value)


#计算bolling指标
class Bollinger:
    #bollinger上轨值:bollinger_up
    #标准差的倍数:std_multi
    def fit(self,data,window,std_multi):
        if window < 2:
            print("variance wrong window!")            
        self.std_data = np.std(data[-window:],ddof = 1)
        self.mid_data = np.mean(data[-window:])
        self.up_data = self.mid_data + std_multi * self.std_data
        self.down_data = self.mid_data - std_multi * self.std_data

    def Up(self,data,window,std_multi):
        self.fit(data,window,std_multi)
        return self.up_data

    def Down(self,data,window,std_multi):
        self.fit(data,window,std_multi)
        return self.down_data



 
class CrossLock :

    CrossOver = False
    CrossUnder = False

    def if_cross_over(self,short,long):

        if (short > long) and (self.CrossOver == False):
 
            self.CrossOver = True
            self.CrossUnder = False

            return True 

        return False


    def if_cross_under(self,short, long) :

        if (short < long) and (self.CrossUnder == False) :

            self.CrossUnder = True
            self.CrossOver = False

            return True


        return False


    def cross_over(self):
    
        return self.CrossOver
    

    def cross_under(self):
    
        return self.CrossUnder
    

    def clear(self):
    
        self.CrossUnder = False
        self.CrossOver = False



