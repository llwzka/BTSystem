from controller import controller

#导入策略
from strategy import strategy

import warnings
warnings.filterwarnings("ignore")

#检测当前是否是运行该main文件
if __name__ == "__main__":

    #获取合约参数
    controller = controller.Controller("contract_info/contract_info.json")

    #获取品种数据
    controller.read_quoter_data("j", "quota_data/J_total_data.csv")
    # controller.read_quoter_data("ru", "quota_data/RU_total_data.csv")


    #注册基于不同品种的策略
    controller.regist_strategy(strategy = strategy.Strategy())
    # controller.regist_strategy(strategy = strategy_cta.Strategy())
    # controller.regist_strategy(strategy = strategy_boll.Strategy())


    #设置初始资金
    controller.get_initial_capital(500000)
    #设置回测范围
    controller.read_start_end_date("2015/06/01", "2018/09/11")
    #回测开始
    controller.start() 

    #输出策略组合的动态权益  
    # controller.total_dynamic_equity()