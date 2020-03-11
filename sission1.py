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
    同时开两单，
    开多单，价格为3.085
    开空单，价格为3.122
    
    持续监控
    如果多单成功，则开空单，价格为3.2
    如果多单不成功，订单不变
    如果空单成功，则开多单，价格为3
    如果空单不成功，订单不变
    '''
    orders = []
    #底部开多
    order1 = {"client_oid": "buy",
              "type": "1",
              "price": "3.085",
              "size": "1",
              "match_price": "0"}
    #顶部开空
    order2 = {"client_oid": "sell",
              "type": "2",
              "price": "3.122",
              "size": "1",
              "match_price": "0"}

    orders.append(order1)
    orders.append(order2)
    orders_data = json.dumps(orders)
    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                       orders_data=orders_data,
                                       leverage=10)
    while True:
        get_orderID=takeorders['order_info']
    #获取订单状态
        for i in get_orderID:
            orderid=i['order_id']
            #print(orderid)
            checkorderinfo = futureAPI.get_order_info('EOS-USD-200327',orderid)
            order_status=checkorderinfo['status']
            order_type=checkorderinfo['type']
            print(orderid,order_status,order_type)
            time.sleep(1)

            #如果2元开多成交，则止损设置1.5元止损

            get_orderID = takeorders['order_info']
            if int(order_status) == 2 :
                if int(order_type) == 1:
                    #价格跌破1.6，则1.6为止损点
                    # 获取当前最新的价格
                    price = futureAPI.get_specific_ticker('EOS-USD-200327')
                    # print(price)
                    #print('EOS最新价格为:', price['last'])
                    # 设置价格为浮点型
                    last_price = float(price['last'])
                    orders = []
                    if last_price <= 3.024 :
                        order1 = {"client_oid": "sell",
                                  "type": "3",
                                  "price": "3.025",
                                  "size": "1",
                                  "match_price": "0"}
                    else :
                        order1 = {"client_oid": "sell",
                                  "type": "3",
                                  "price": "3.122",
                                  "size": "1",
                                  "match_price": "0"}

                    orders.append(order1)
                    orders_data = json.dumps(orders)
                    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                                       orders_data=orders_data,
                                                       leverage=10)
                    get_orderID = takeorders['order_info']
                # 如果4元开空成交，则止损设置5.5元止损
                if int(order_type) == 2:
                    #价格涨破6，则6为止损点,否则2元平空
                    # 获取当前最新的价格
                    price = futureAPI.get_specific_ticker('EOS-USD-200327')
                    # print(price)
                    print('EOS最新价格为:', price['last'])
                    # 设置价格为浮点型
                    last_price = float(price['last'])
                    orders = []
                    if last_price >= 3.185:
                        order1 = {"client_oid": "buy",
                                  "type": "4",
                                  "price": "3.184",
                                  "size": "1",
                                  "match_price": "0"}
                    else:
                        order1 = {"client_oid": "sell",
                                  "type": "4",
                                  "price": "3.085",
                                  "size": "1",
                                  "match_price": "0"}

                    orders.append(order1)
                    orders_data = json.dumps(orders)
                    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                                       orders_data=orders_data,
                                                       leverage=10)
                    get_orderID = takeorders['order_info']
                if int(order_type) == 3:
                    print('平多已经成交,设置开多新订单')
                    orders = []
                    order1 = {"client_oid": "buy",
                              "type": "1",
                              "price": "3.085",
                              "size": "1",
                              "match_price": "0"}
                    orders.append(order1)
                    orders_data = json.dumps(orders)
                    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                                       orders_data=orders_data,
                                                       leverage=10)
                    print('EOS期货新多单下单成功')
                    orderID = takeorders['order_info'][0]['order_id']
                    # 获取订单状态
                    # checkorderinfo = futureAPI.get_order_info('EOS-USD-200327', orderID)
                    # print(checkorderinfo)
                    time.sleep(1)
                if int(order_type) == 4:
                    print('平空已经成交,设置开空新订单')
                    orders = []
                    order2 = {"client_oid": "sell",
                              "type": "2",
                              "price": "3.122",
                              "size": "1",
                              "match_price": "0"}
                    orders.append(order2)
                    orders_data = json.dumps(orders)
                    takeorders = futureAPI.take_orders('EOS-USD-200327',
                                                       orders_data=orders_data,
                                                       leverage=10)
                    print('EOS期货新空单下单成功')
                    orderID = takeorders['order_info'][0]['order_id']
                    # 获取订单状态
                    # checkorderinfo = futureAPI.get_order_info('EOS-USD-200327', orderID)
                    # print(checkorderinfo)
                    time.sleep(1)
            else:
                print("订单无变化")
                time.sleep(2)

