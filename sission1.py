import okex.account_api as account
import okex.ett_api as ett
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import json
import time

if __name__ == '__main__':
    #设置ID
    api_key = '646f4929-682b-43f9-9892-4f55d6001dd6'
    seceret_key = '843B6EE7FEB5346462AEBBB83F0C210C'
    passphrase = 'ibm11ibm***'
    #设置交易类型函数
    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
    print('开始运行交易系统')
    #获取当前最新的价格
    price = futureAPI.get_specific_ticker('EOS-USD-200327')
    #print(price)
    print('EOS最新价格为:',price['last'])
    #设置价格为浮点型
    last_price=float(price['last'])

    result = futureAPI.get_order_list('EOS-USD-200327', '2')
    print(result)

    '''
    同时开两单，
    开多单，价格为3.8
    开空单，价格为3.821
    
    持续监控
    如果多单成功，则开空单，价格为3.822
    如果多单不成功，订单不变
    如果空单成功，则开多单，价格为3.854
    如果空单不成功，订单不变
    '''
    orders = []

    order1 = {"client_oid": "buy",
              "type": "1",
              "price": "3.811"
              "size": "2",
              "match_price": "0"}

    order2 = {"client_oid": "sell",
              "type": "2",
              "price": "3.853",
              "size": "2",
              "match_price": "0"}

    orders.append(order1)
    orders.append(order2)
    orders_data = json.dumps(orders)
    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                       orders_data=orders_data,
                                       leverage=10)

