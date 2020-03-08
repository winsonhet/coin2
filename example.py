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

    '''
    根据报价买入
    监控订单
    如果成交，则新建订单卖出
    如果未成交。继续监控
    '''

    # take orders
    orders = []

    order1 = {"client_oid": "buy",
              "type": "1",
              "price": last_price-0.05,
              "size": "3",
              "match_price": "0"}
    orders.append(order1)
    orders_data = json.dumps(orders)
    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                       orders_data=orders_data,
                                       leverage=10)
    print('EOS期货下单成功')
    # orderID=takeorders['order_info'][0]['order_id']
    #获取订单状态
    #checkorderinfo=futureAPI.get_order_info('EOS-USD-200327',orderID)
    # print(checkorderinfo)
    #获取订单状态


    #持续循环
    while True:

        # 获取当前最新的价格
        #price = futureAPI.get_specific_ticker('EOS-USD-200327')
        # print(price)
        #print('EOS最新价格为:', price['last'])
        # 设置价格为浮点型
       # last_price = float(price['last'])
        # 获取订单状态
        orderID = takeorders['order_info'][0]['order_id']
        checkorderinfo = futureAPI.get_order_info('EOS-USD-200327', orderID)
        # print(checkorderinfo)
        # 获取订单状态
        get_order_type = checkorderinfo['type']
        get_order_state = checkorderinfo['state']
        get_order_price = float(checkorderinfo['price'])
        #print(get_order_type)
        #print(get_order_state)
        #print('下单价格为:', get_order_price)
        #检查订单状态，如果订单成交，则平多
        #平多后，则再次新建订单    #获取订单状态
        if int(get_order_state) == 2:
            if int(get_order_type) == 1:
                print('开多已经成交,设置平多新订单')
                orders = []
                order1 = {"client_oid": "sell",
                          "type": "3",
                          "price": get_order_price+0.004,
                          "size": "3",
                          "match_price": "0"}
                orders.append(order1)
                orders_data = json.dumps(orders)
                takeorders = futureAPI.take_orders('EOS-USD-200327',
                                                   orders_data=orders_data,
                                                   leverage=10)
                print('EOS期货下单成功')
                orderID = takeorders['order_info'][0]['order_id']
                time.sleep(1)
                # 获取订单状态
                #checkorderinfo = futureAPI.get_order_info('EOS-USD-200327', orderID)
                # print(checkorderinfo)
            if int(get_order_type) == 3:
                print('平多已经成交,设置开多新订单')
                # 获取当前最新的价格
                time.sleep(4)
                price = futureAPI.get_specific_ticker('EOS-USD-200327')
                # print(price)
                print('EOS最新价格为:', price['last'])
                # 设置价格为浮点型
                last_price = float(price['last'])

                orders = []
                order1 = {"client_oid": "buy2",
                          "type": "1",
                          "price": last_price-0.002,
                          "size": "3",
                          "match_price": "0"}
                orders.append(order1)
                orders_data = json.dumps(orders)
                takeorders = futureAPI.take_orders('EOS-USD-200327',
                                                   orders_data=orders_data,
                                                   leverage=10)
                print('EOS期货下单成功')
                orderID = takeorders['order_info'][0]['order_id']
                # 获取订单状态
                #checkorderinfo = futureAPI.get_order_info('EOS-USD-200327', orderID)
                # print(checkorderinfo)
                time.sleep(1)
        else:
            print('订单状态未改变')
            time.sleep(30)






